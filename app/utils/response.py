class ResponseHandler:
    @staticmethod
    def success(message, data=None):
        response = {"success": True, "message": message}
        if data:
            response["data"] = data
        return response, 200

    @staticmethod
    def error(message, status=400):
        return {"success": False, "message": message}, status
