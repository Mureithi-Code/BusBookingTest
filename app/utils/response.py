from flask import jsonify

class ResponseHandler:
    @staticmethod
    def success(message, data=None, status=200):
        response = {"success": True, "message": message}
        if data:
            response["data"] = data
        return jsonify(response), status

    @staticmethod
    def error(message, status=400):
        return jsonify({"success": False, "message": message}), status
