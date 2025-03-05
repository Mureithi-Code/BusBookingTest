class ResponseHandler:
    @staticmethod
    def success(message, data=None, status=200):
        """
        Standard success response.
        Always returns a `data` key, even if no data (as an empty object).
        Allows for overriding the status code (e.g., 201 for created).
        """
        response = {
            "success": True,
            "message": message,
            "data": data if data is not None else {}
        }
        return response, status

    @staticmethod
    def error(message, status=400):
        """
        Standard error response.
        Always returns a `data` key set to None.
        """
        return {
            "success": False,
            "message": message,
            "data": None
        }, status
