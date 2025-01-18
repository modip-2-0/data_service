from typing import Any
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema


class PyObjectId(ObjectId):
    """
    Custom type for handling MongoDB ObjectId fields in Pydantic models.
    Extends bson.ObjectId to provide Pydantic integration.
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        """
        Defines the core schema for Pydantic validation of ObjectId.
        
        Args:
            _source_type: Source type information (unused)
            _handler: Schema handler (unused)
            
        Returns:
            CoreSchema: Schema for ObjectId validation
        """
        def validate(value: str) -> ObjectId:
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")
            return ObjectId(value)
    
        return core_schema.no_info_plain_validator_function(
            function=validate,
            serialization=core_schema.to_string_ser_schema(),
        )
    
    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """
        Defines the JSON schema for ObjectId serialization.
        
        Args:
            _core_schema: Core schema definition
            handler: JSON schema handler
            
        Returns:
            JsonSchemaValue: Schema for JSON serialization
        """
        return handler(core_schema.str_schema())


class MongoModel(BaseModel):
    """
    Base model for MongoDB documents.
    Provides common functionality for all MongoDB-backed models.
    
    Attributes:
        id (PyObjectId): MongoDB document _id field
    """
    
    id: PyObjectId = Field(alias="_id")

    model_config = ConfigDict(arbitrary_types_allowed=True)