import os
from dotenv import load_dotenv
import sys
from src.config import get_workdir
from pathlib import Path


load_dotenv()

# Try to get WORKDIR from environment variable
WORKDIR = os.getenv("WORKDIR")

# If WORKDIR is not set or doesn't exist, use the parent directory of this file
if not WORKDIR or not Path(WORKDIR).exists():
    WORKDIR = str(Path(__file__).resolve().parent.parent)
    print(f"Warning: WORKDIR not set or invalid. Using: {WORKDIR}")

# Ensure WORKDIR exists
if not Path(WORKDIR).exists():
    raise FileNotFoundError(f"WORKDIR directory does not exist: {WORKDIR}")

# Change to the WORKDIR
os.chdir(WORKDIR)

# Add WORKDIR to Python path
sys.path.append(WORKDIR)

from pydantic import BaseModel, field_validator, Field
import re
from typing import Dict 

class IndexNameStructure(BaseModel):
    index_name: str = Field(description="Lower case name of the index you want to create")


    @field_validator('index_name')
    def check_letters_lowercase(cls, v):
        if not re.fullmatch(r"^[a-z]+$", v):
            raise ValueError('index_name must be only letters in lowercase')
        return v

class ExpectedNewData(BaseModel):
    new_info: Dict[str, str] = Field(description="Expected a pair key:value of question and answer.")


    @field_validator('new_info')
    def check_lowercase(cls, v):
        if set(v.keys()) != {'question','answer'}:
            raise ValueError("The structure of the dictionary should be {'question':'...,' 'answer':'...'}")
        return v