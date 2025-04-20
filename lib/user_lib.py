import json
from routers.user import UserCreate
from fastapi import HTTPException

class UserList:
    def __init__(self, config_path):
        self.config_path = config_path
        self.users = self.load_users()

    def load_users(self):
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def get_all_user(self):
        return self.users

    def get_user_by_uid(self, uid):
        for user in self.users:
            if user['uid'] == uid:
                return user
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    def save_user(self):
        with open(self.config_path, "w") as f:
            json.dump(self.users, f, indent=4)

    def create_user(self, user: UserCreate):
        new_uid = max([int(u["uid"] for u in self.users)])
        new_data = {
            "uid": str(new_uid),
            "username": user.username,
            "password": user.password,
            "primogems": 0,
            "pity": 0,
            "four_star_pity": 0,
            "rate_on": False,
            "four_star_rate_on": False,
            "rarity_weight": {"3-star": 94, "4-star": 5, "5-star": 1},
        }
        self.users.append(new_data)
        self.save_user()
        return new_data

    def update_user(self, uid: str, user:UserCreate):
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