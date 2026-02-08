"""
API Testing Tool for CrewAI
A comprehensive tool for testing REST APIs with various HTTP methods and validations.
"""

import json
import time
from typing import Any, Dict, List, Optional, Union
from enum import Enum

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class HttpMethod(str, Enum):
    """Supported HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class APITestResult(BaseModel):
    """Model for API test results."""
    success: bool
    status_code: int
    response_time_ms: float
    response_body: Optional[Union[Dict, List, str]] = None
    headers: Dict[str, str]
    error: Optional[str] = None
    validations: List[str] = Field(default_factory=list)



class APITestTool(BaseTool):

    """API Test Tool for autonomous tester.
        A tool for testing REST APIs with comprehensive validation capabilities.
        
        Supports:
        - All common HTTP methods (GET, POST, PUT, PATCH, DELETE, etc.)
        - Request headers and authentication
        - Request body (JSON, form data, raw)
        - Response validation (status codes, headers, body content)
        - Response time measurement
        - JSON path validation
    """
    
    name: str = "API Test Tool"
    description: str = """
    Test REST APIs with various HTTP methods and validate responses.
    
    Input should be a JSON string with the following structure:
    {
        "url": "https://api.example.com/endpoint",
        "method": "GET|POST|PUT|PATCH|DELETE",
        "headers": {"Content-Type": "application/json"},  # optional
        "body": {"key": "value"},  # optional, for POST/PUT/PATCH
        "params": {"query_param": "value"},  # optional, URL parameters
        "auth": {"type": "bearer", "token": "your_token"},  # optional
        "timeout": 30,  # optional, default 30 seconds
        "validate": {  # optional validations
            "status_code": 200,
            "contains": "expected text",
            "json_path": {"path.to.field": "expected_value"}
        }
    }
    
    Returns a detailed test result including status code, response time, body, and validation results.
    """
    def _parse_input(self, query: str) -> Dict[str, Any]:
        """Parse the input query string to extract API test parameters."""
        try:
            if isinstance(query, str):
                params = json.loads(query)
            else:
                params = query
            return params
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON input: {str(e)}")
    
    def _prepare_auth(self, auth_config: Optional[Dict[str, str]]) -> Optional[Any]:
        """Prepare authentication based on config."""
        if not auth_config:
            return None
        
        auth_type = auth_config.get("type", "").lower()
        
        if auth_type == "bearer":
            token = auth_config.get("token")
            return {"Authorization": f"Bearer {token}"}
        elif auth_type == "basic":
            from requests.auth import HTTPBasicAuth
            username = auth_config.get("username")
            password = auth_config.get("password")
            return HTTPBasicAuth(username, password)
        elif auth_type == "api_key":
            key_name = auth_config.get("key_name", "X-API-Key")
            key_value = auth_config.get("key_value")
            return {key_name: key_value}
        
        return None
    
    def _get_json_path_value(self, data: Any, path: str) -> Any:
        """Extract value from nested JSON using dot notation path."""
        keys = path.split('.')
        value = data
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            elif isinstance(value, list) and key.isdigit():
                index = int(key)
                value = value[index] if index < len(value) else None
            else:
                return None
            
            if value is None:
                return None
        
        return value
    
    def _validate_response(
        self, 
        response: requests.Response, 
        validations: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Validate response against specified criteria."""
        validation_results = []
        
        if not validations:
            return validation_results
        
        expected_status = validations.get("status_code")
        if expected_status is not None:
            if response.status_code == expected_status:
                validation_results.append(f"✓ Status code {response.status_code} matches expected")
            else:
                validation_results.append(
                    f"✗ Status code {response.status_code} != expected {expected_status}"
                )
        
        contains_text = validations.get("contains")
        if contains_text:
            if contains_text in response.text:
                validation_results.append(f"✓ Response contains '{contains_text}'")
            else:
                validation_results.append(f"✗ Response does not contain '{contains_text}'")
        
        json_path_validations = validations.get("json_path", {})
        if json_path_validations:
            try:
                response_json = response.json()
                for path, expected_value in json_path_validations.items():
                    actual_value = self._get_json_path_value(response_json, path)
                    if actual_value == expected_value:
                        validation_results.append(
                            f"✓ JSON path '{path}' = {expected_value}"
                        )
                    else:
                        validation_results.append(
                            f"✗ JSON path '{path}' = {actual_value} != expected {expected_value}"
                        )
            except json.JSONDecodeError:
                validation_results.append("✗ Response is not valid JSON")
        
        header_validations = validations.get("headers", {})
        for header_name, expected_value in header_validations.items():
            actual_value = response.headers.get(header_name)
            if actual_value == expected_value:
                validation_results.append(f"✓ Header '{header_name}' = {expected_value}")
            else:
                validation_results.append(
                    f"✗ Header '{header_name}' = {actual_value} != expected {expected_value}"
                )
        
        max_response_time = validations.get("max_response_time_ms")
        if max_response_time is not None:
            response_time_ms = response.elapsed.total_seconds() * 1000
            if response_time_ms <= max_response_time:
                validation_results.append(
                    f"✓ Response time {response_time_ms:.2f}ms <= {max_response_time}ms"
                )
            else:
                validation_results.append(
                    f"✗ Response time {response_time_ms:.2f}ms > {max_response_time}ms"
                )
        
        return validation_results
    
    def _run(self, query: str) -> str:
        """
        Execute the API test with the given parameters.
        
        Args:
            query: JSON string containing API test parameters
            
        Returns:
            str: JSON string containing test results
        """
        try:
            params = self._parse_input(query)
            
            url = params.get("url")
            if not url:
                raise ValueError("URL is required")
            
            method = params.get("method", "GET").upper()
            headers = params.get("headers", {})
            body = params.get("body")
            query_params = params.get("params", {})
            auth_config = params.get("auth")
            timeout = params.get("timeout", 30)
            validations = params.get("validate")
            
            auth = self._prepare_auth(auth_config)
            if auth and isinstance(auth, dict):
                headers.update(auth)
                auth = None
            
            start_time = time.time()
            
            request_kwargs = {
                "headers": headers,
                "params": query_params,
                "timeout": timeout,
                "auth": auth
            }
            
            if method in ["POST", "PUT", "PATCH"] and body is not None:
                if isinstance(body, (dict, list)):
                    request_kwargs["json"] = body
                else:
                    request_kwargs["data"] = body
            
            response = requests.request(method, url, **request_kwargs)
            
            end_time = time.time()
            response_time_ms = (end_time - start_time) * 1000
            
            try:
                response_body = response.json()
            except json.JSONDecodeError:
                response_body = response.text
            
            validation_results = self._validate_response(response, validations)
            
            success = response.status_code < 400
            if validations and validation_results:
                success = success and not any("✗" in v for v in validation_results)
            
            result = APITestResult(
                success=success,
                status_code=response.status_code,
                response_time_ms=response_time_ms,
                response_body=response_body,
                headers=dict(response.headers),
                validations=validation_results
            )
            
            return json.dumps(result.model_dump(), indent=2)
            
        except requests.exceptions.RequestException as e:
            error_result = APITestResult(
                success=False,
                status_code=0,
                response_time_ms=0.0,
                headers={},
                error=f"Request failed: {str(e)}"
            )
            return json.dumps(error_result.model_dump(), indent=2)
            
        except Exception as e:
            error_result = APITestResult(
                success=False,
                status_code=0,
                response_time_ms=0.0,
                headers={},
                error=f"Unexpected error: {str(e)}"
            )
            return json.dumps(error_result.model_dump(), indent=2)
