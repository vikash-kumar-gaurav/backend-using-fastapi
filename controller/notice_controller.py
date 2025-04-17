from fastapi import HTTPException
from models.noticemodel import createNotice,availableNotice
from bson import ObjectId
class NoticeController:
    @staticmethod

    #new notice will be created here
    async def create_notice(db,notice_data:createNotice, current_user):
        try:
            print(notice_data)
            
            if not notice_data.title or not notice_data.content:
                raise HTTPException(status_code=404, detail="Please provide notice details")
            
            if current_user["role"] != "admin":
                raise HTTPException(status_code=403, detail="you are not authorized to create a notice only admin can")
            
            notice_dict = notice_data.dict()
            #we will add who created it 

            notice_dict["created_by"] = current_user["_id"] 

            result = await db["notices"].insert_one(notice_dict)
            
            return {
                "msg":"notice created",
                "notice":str(result)
            }

        except HTTPException as http_err:
            raise http_err

        except Exception as error:
            print("error from create_notice from controller", error)
            raise HTTPException(status_code=500, detail="Server Error try later")


    # now see the notice usually admin or students
    @staticmethod
    async def available_notice(db):
        try:
           

            notices = await db["notices"].find().sort("created_at", -1).to_list(length=100)
            
            

            for n in notices:
                 

                if "_id" in n:
                    n["_id"]= str(n["_id"])
                # If created_by exists, fetch user details
                if "created_by" in n:
                    try:
                        user_obj_id = ObjectId(n["created_by"])  # convert str to ObjectId
                        user = await db["users"].find_one({"_id": user_obj_id})
                        if user:
                            n["created_by"] = {
                                "id": str(user["_id"]),
                                "name": user.get("name", "Unknown"),
                                "email": user.get("email", "N/A")
                            }
                    except Exception as e:
                        # In case the ObjectId conversion fails or user not found
                        n["created_by"] = {
                            "id": n["created_by"],
                            "name": "Unknown",
                            "email": "N/A"
                        }
                    
                    
                      

            return {"notice": notices}         
        except Exception as error:
            print("error from available notice from controller",error)
            raise HTTPException(status_code=500,detail="server Error try later")  