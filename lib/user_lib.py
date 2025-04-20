import json
from models.models import UserCreate
from fastapi import HTTPException

class UserList:
    def __init__(self, user_path, history_path):
        self.user_path = user_path
        self.users = self.load_users()
        self.keys_to_remove = ["password", "rarity_weight"]
        self.history_path = history_path

    def load_users(self):
        with open(self.user_path, "r") as f:
            return json.load(f)

    def save_user(self):
        with open(self.user_path, "w") as f:
            json.dump(self.users, f, indent=4)

    def get_all_user(self):
        result = []
        for user in self.users:
            for key in self.keys_to_remove:
                user.pop(key, None)
            result.append(user)
        return result

    def get_user_by_uid(self, uid):
        for i, u in enumerate(self.users):
            if u["uid"] == uid:
                user = self.users[i].copy()
                for key in self.keys_to_remove:
                    user.pop(key, None)
                return user
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    def create_user(self, user: UserCreate):
        new_uid = (
            str(int(max([u["uid"] for u in self.users])) + 1)
            if self.users
            else "800000001"
        )
        new_data = {
            "uid": new_uid,
            "username": user.username,
            "password": user.password,
            "primogems": 1000000,
            "pity": 0,
            "four_star_pity": 0,
            "is_rate_on": False,
            "four_star_rate_on": False,
            "rarity_weight": {"3-star": 94, "4-star": 5, "5-star": 1},
        }
        self.users.append(new_data)
        self.save_user()
        return self.get_user_by_uid(new_uid)

    def update_user(self, uid: str, user: UserCreate):
        for i, u in enumerate(self.users):
            if u["uid"] == uid:
                self.users[i].update(user.model_dump())
                self.users[i]["uid"] = uid
                self.save_user()
                return self.users[i]
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    def save_user_rarity_weight(self, uid: str, rarity_weight: dict):
        for i, u in enumerate(self.users):
            if u["uid"] == uid:
                self.users[i]["rarity_weight"] = rarity_weight
                self.save_user()
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    def delete_user(self, uid: str):
        for i, u in enumerate(self.users):
            if u["uid"] == uid:
                del self.users[i]
                self.save_user()
                return {"message": f"User dengan ID {uid} telah dihapus"}
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    def get_user_history(self, uid: str):
        with open(self.history_path, "r") as f:
            all_history = json.load(f)
        result = []
        for history in all_history:
            if history["uid"] == uid:
                result.append(history)
        return result
