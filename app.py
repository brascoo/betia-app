from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional
import jwt
from datetime import datetime, timedelta
import bcrypt

from models import Base, User, Pick, Parley, ParleyLeg

# Configuración Base de Datos
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Configuración Seguridad
SECRET_KEY = "super_secret_betia_key_change_in_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 1 semana

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(title="BETIA Pro API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencias
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auth Utils
def verify_password(plain_password, hashed_password):
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_password_hash(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# Modelos Pydantic (Schemas)
class UserCreate(BaseModel):
    username: str
    password: str

class PickCreate(BaseModel):
    sport: str
    match: str
    selection: str
    odds: float
    stake: float
    date: str
    analysis: Optional[str] = None
    confidence: int

class PickUpdate(BaseModel):
    status: str

class LegCreate(BaseModel):
    match: str
    selection: str
    odds: float

class ParleyCreate(BaseModel):
    name: str
    stake: float
    date: str
    legs: List[LegCreate]

class ParleyUpdate(BaseModel):
    status: str

# Endpoints de Autenticación
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "bankroll": user.bankroll}

# Endpoints Bankroll
@app.post("/api/bankroll")
def update_bankroll(amount: float, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.bankroll = amount
    db.commit()
    return {"bankroll": current_user.bankroll}

@app.get("/api/bankroll")
def get_bankroll(current_user: User = Depends(get_current_user)):
    return {"bankroll": current_user.bankroll}

# Endpoints Picks
@app.get("/api/picks")
def read_picks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    picks = db.query(Pick).filter(Pick.user_id == current_user.id).all()
    return picks

@app.post("/api/picks")
def create_pick(pick: PickCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_pick = Pick(**pick.dict(), user_id=current_user.id)
    db.add(db_pick)
    db.commit()
    db.refresh(db_pick)
    return db_pick

@app.put("/api/picks/{pick_id}")
def update_pick(pick_id: int, pick_update: PickUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_pick = db.query(Pick).filter(Pick.id == pick_id, Pick.user_id == current_user.id).first()
    if not db_pick:
        raise HTTPException(status_code=404, detail="Pick not found")
    db_pick.status = pick_update.status
    db.commit()
    db.refresh(db_pick)
    return db_pick

# Endpoints Parleys
@app.get("/api/parleys")
def read_parleys(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Include legs
    parleys = db.query(Parley).filter(Parley.user_id == current_user.id).all()
    result = []
    for p in parleys:
        p_dict = {
            "id": p.id, "name": p.name, "stake": p.stake, "status": p.status, "date": p.date,
            "legs": [{"id": l.id, "match": l.match, "selection": l.selection, "odds": l.odds, "status": l.status} for l in p.legs]
        }
        result.append(p_dict)
    return result

@app.post("/api/parleys")
def create_parley(parley: ParleyCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_parley = Parley(name=parley.name, stake=parley.stake, date=parley.date, user_id=current_user.id)
    db.add(db_parley)
    db.commit()
    db.refresh(db_parley)
    
    for leg in parley.legs:
        db_leg = ParleyLeg(**leg.dict(), parley_id=db_parley.id)
        db.add(db_leg)
    db.commit()
    return {"message": "Parley created"}

@app.put("/api/parleys/{parley_id}")
def update_parley(parley_id: int, parley_update: ParleyUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_parley = db.query(Parley).filter(Parley.id == parley_id, Parley.user_id == current_user.id).first()
    if not db_parley:
        raise HTTPException(status_code=404, detail="Parley not found")
    
    status = parley_update.status
    db_parley.status = status
    
    # Update legs based on parley status
    leg_status = "won" if status == "ganado" else "lost" if status == "perdido" else "pending"
    for leg in db_parley.legs:
        leg.status = leg_status
        
    db.commit()
    return {"message": "Parley updated"}
