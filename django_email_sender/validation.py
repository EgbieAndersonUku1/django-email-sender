import inspect
from django.utils.translation import gettext_lazy as _

from inspect import signature
from typing import Callable, Any, Dict, TypedDict
from typing import get_origin, get_args

from django_email_sender.exceptions import IncorrectEmailModelAddedError
from django_email_sender.messages import EmailClassNames


def validate_custom_formatter(formatter: Callable) -> Callable:
    """
    Validates the user-provided custom formatter function.
    
    Args:
       formatter (func) : A callable function that allows the user to format their errors
       
    It must:
    - Be callable
    - Accept 1 or 2 parameters
    - Correctly handle an Exception object (and optionally a traceback string)
    
    """
    if not callable(formatter):
        raise TypeError(_("Custom formatter must be a callable function."))

    sig           = signature(formatter)
    params_length = len(list(sig.parameters))

    if params_length == 2:
        
        # User function expects (Exception, trace)
        def test_call():
            return formatter(Exception("Test exception"), "Dummy traceback")

    elif params_length == 1:
        
        # User function expects (Exception) only
        def test_call():
            return formatter(Exception("Test exception"))

        # Wrap it to always behave as two-argument later
        def wrapped_formatter(exc: Exception, trace: str) -> str:
            return formatter(exc)
        
        formatter = wrapped_formatter

    else:
        raise TypeError(_("Custom formatter must accept either one parameter (Exception) or two parameters (Exception, str)."))

    try:
        result = test_call()
        if not isinstance(result, str):
            raise TypeError(_("Custom formatter must return a string."))
    except Exception as e:
        raise TypeError(_("""
                          Error while validating custom formatter: {e} 
                          Make sure your formatter accepts the correct arguments and returns a string.
                        """
                        ).format(e=e)
        )

    return formatter


def _types_match(expected, actual):
    if expected == actual:
        return True
    if get_origin(expected) == get_origin(actual):
        return get_args(expected) == get_args(actual)
    return False



class ParamContract(TypedDict):
    method: str
    params: Dict[str, type]

EmailContract = Dict[str, ParamContract]


def validate_method_signature(obj: Any, method_name: str, expected_params: Dict[str, type]) -> EmailContract:
    """
    Validates that a method on an object has the expected parameters and type annotations.

    Args:
        obj (Any): The object containing the method.
        method_name (str): The name of the method to validate.
        expected_params (Dict[str, type]): A dictionary of expected parameter names and types.

    Returns:
        bool: True if the method exists, is callable, and matches the expected signature; False otherwise.
    """
    method = getattr(obj, method_name, None)
    
    if not callable(method):
        return False

    try:
        sig = inspect.signature(method)
    except ValueError:
        return False  

    # Loop through the expected parameters and check if they match in type
    for name, expected_type in expected_params.items():
        param = sig.parameters.get(name)
        if param is None:
            return False
    
        if param.annotation is not inspect.Parameter.empty:
            # Check if the annotation matches the expected type
            if not _types_match(expected_type, param.annotation):
                return False
    return True


def validate_custom_email_model(custom_model, model_to_validate_against):
    
    if not custom_model or not model_to_validate_against:
        raise IncorrectEmailModelAddedError(_("Custom model or the model to validate against cannot be None"))
    
    if isinstance(custom_model, model_to_validate_against):
        raise IncorrectEmailModelAddedError(_("You cannot add the instance of the model. Add the model without '()' "))
    
    if not issubclass(custom_model, model_to_validate_against):
        raise IncorrectEmailModelAddedError(_("Model added is not a subclass of EmailBaseLog. Model must inherit from EmailBaseLog"))
    
    class_name = custom_model.__class__.__name__
    
    if custom_model.__class__.__name__ == EmailClassNames.EMAIL_MODEL:
        raise IncorrectEmailModelAddedError(_("Model must not be the EmailLog model: %(class_name)s"), class_name=class_name)
    
    return True

        
    
    