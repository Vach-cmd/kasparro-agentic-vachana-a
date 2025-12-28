from abc import ABC, abstractmethod
from typing import Any, Dict
import time
from ..exceptions import AgentExecutionError


class BaseAgent(ABC):
    """
    Base class for all agents in the system.
    Each agent has a single responsibility and defined input/output contract.
    """
    
    def __init__(self, name: str, max_retries: int = 3):
        self.name = name
        self.state: Dict[str, Any] = {}
        self.max_retries = max_retries
        self.execution_count = 0
        self.total_execution_time = 0.0
    
    @abstractmethod
    def execute(self, input_data: Any) -> Any:
        """
        Execute the agent's primary responsibility.
        
        Args:
            input_data: Input data conforming to agent's contract
            
        Returns:
            Output data conforming to agent's contract
            
        Raises:
            AgentExecutionError: If execution fails after retries
        """
        pass
    
    def execute_with_retry(self, input_data: Any) -> Any:
        """
        Execute with retry logic for robustness.
        
        Args:
            input_data: Input data
            
        Returns:
            Execution result
            
        Raises:
            AgentExecutionError: If all retries fail
        """
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                result = self.execute(input_data)
                execution_time = time.time() - start_time
                
                self.execution_count += 1
                self.total_execution_time += execution_time
                
                return result
                
            except Exception as e:
                last_error = e
                self.log(f"Attempt {attempt + 1}/{self.max_retries} failed: {str(e)}")
                
                if attempt < self.max_retries - 1:
                    time.sleep(0.1 * (attempt + 1))  # Exponential backoff
        
        raise AgentExecutionError(
            f"{self.name} failed after {self.max_retries} attempts: {str(last_error)}"
        )
    
    def get_name(self) -> str:
        """Get agent name"""
        return self.name
    
    def validate_input(self, input_data: Any) -> bool:
        """
        Validate input data. Override in subclasses for specific validation.
        
        Args:
            input_data: Data to validate
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If validation fails
        """
        if input_data is None:
            raise ValueError(f"{self.name}: Input data cannot be None")
        return True
    
    def log(self, message: str, level: str = "info") -> None:
        """
        Log agent activity.
        
        Args:
            message: Log message
            level: Log level (info, warning, error)
        """
        prefix = f"[{self.name}]"
        if level == "error":
            print(f"{prefix} ERROR: {message}")
        elif level == "warning":
            print(f"{prefix} WARNING: {message}")
        else:
            print(f"{prefix} {message}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        avg_time = (
            self.total_execution_time / self.execution_count 
            if self.execution_count > 0 else 0
        )
        
        return {
            "name": self.name,
            "executions": self.execution_count,
            "total_time": round(self.total_execution_time, 3),
            "average_time": round(avg_time, 3)
        }
