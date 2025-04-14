""" Module that includes SignUtil class for signing API requests """
import hashlib
from typing import Dict, List, Optional


class SignUtil:
    """ Sign Util class to manage API request signing to Smart Tyre website """
    @staticmethod
    def sign(headers: Optional[Dict[str, str]] = None,
             body: Optional[str] = None,
             params: Optional[Dict[str, List[str]]] = None,
             paths: Optional[List[str]] = None,
             sign_key: str = "") -> str:
        """
        Generate a signature for API requests by concatenating and
        hashing various request components.

        Args:
            headers: HTTP request headers
            body: The request body content
            params: URL query parameters where each parameter can have multiple values
            paths: Path parameters
            sign_key: Secret key used for signing

        Returns:
            MD5 hash of the concatenated string as a hex digest
        """
        components = []

        # Process headers (sorted by key)
        if headers:
            for key in sorted(headers.keys()):
                components.append(f"{key}={headers[key]}&")

        # Add body if present
        if body:
            components.append(f"{body}&")

        # Process query parameters (sorted by key)
        if params:
            for key in sorted(params.keys()):
                # Sort the parameter values
                sorted_values = sorted(params[key])
                param_value = ",".join(sorted_values)
                components.append(f"{key}={param_value}&")

        # Process path parameters
        if paths:
            sorted_paths = sorted(paths)
            path_values = ",".join(sorted_paths)
            components.append(f"{path_values}&")

        # Add sign key
        components.append(sign_key)

        # Join all components and calculate MD5 hash
        message = "".join(components)
        md5_hash = hashlib.md5(message.encode('utf-8')).hexdigest()

        return md5_hash