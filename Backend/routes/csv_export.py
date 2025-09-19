from flask_restful import Resource
from flask import send_file
from flask_jwt_extended import jwt_required,get_jwt_identity
from Backend.tasks.user_task import export_csv
from Backend.utils.jwt_utils import user_required
import os

class CSVExport(Resource):
    @jwt_required()
    @user_required
    def get(self):
        user_id=get_jwt_identity()
        file_name=f"user_{user_id}_export.csv"

        task=export_csv.delay(user_id)

        print('its exporting')
        
        return {'message':'CSV export task started','task_id':task.id,'file_name':file_name},202
    
class CSVDownload(Resource):
    @jwt_required()
    @user_required
    def get(self,file_name):
        user_id=get_jwt_identity()
        file=f"user_{user_id}_export.csv"

        if file_name!=file:
            return {"message":"You are not authenticated for this file"},403
        
        file_path = os.path.abspath(os.path.join('exports', file))

        print(file_path)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return {"message":"Either file has not been downloaded yet in server or you have not exported the file"},404