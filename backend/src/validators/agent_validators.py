from pydantic import constr, BaseModel, Field, validator
import re


class DateTimeModel(BaseModel):
    """
    The way the date should be structured and formatted
    """
    date: str = Field(..., description="Propertly formatted date", pattern=r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$')

    @validator("date")
    def check_format_date(cls, v):
        if not re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$', v):
            raise ValueError("The date should be in format 'YYYY-MM-DD HH:MM'")
        return v
class DateModel(BaseModel):
    """
    The way the date should be structured and formatted
    """
    date: str = Field(..., description="Propertly formatted date", pattern=r'^\d{4}-\d{2}-\d{2}$')

    @validator("date")
    def check_format_date(cls, v):
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
            raise ValueError("The date must be in the format 'YYYY-MM-DD'")
        return v

    
class IdentificationNumberModel(BaseModel):
    """
    The way the ID should be structured and formatted
    """
    id: str = Field(..., description="identification number without dots")

    @validator("id")
    def check_format_id(cls, v):
        if not re.match(r'^\d{7,8}$', v):
            raise ValueError("The ID number should be a number of 7 or 8 digits")
        return int(v)  # Convert to integer after validation
    
