import json
from models.models import UserCreate
from fastapi import HTTPException
import os
from lib.file_path import Path

class UserList:
    def __init__(self):
        self.user_path = Path.USER_PATH
        self.users = self.load_users()
        self.keys_to_remove = ["password", "rarity_weight"]
        self.history_path = Path.HISTORY_PATH

    def load_users(self):
        try:
            with open(self.user_path, "r") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("User file must contain list")
                return data

        except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
            print(f"[Error] Failed to load user from {self.user_path}: {e}")
            return []

    def save_user(self):
        try:
            with open(self.user_path, "w") as f:
                json.dump(self.users, f, indent=4)
        except (PermissionError, TypeError, OSError, json.JSONDecodeError) as e:
            print(f"[Error]: Gagal menyimpan user di {self.user_path}: {e}")

    def get_all_user(self):
        self.users = self.load_users()
        result = []
        for user in self.users:
            user_copy = user.copy()
            for key in self.keys_to_remove:
                user_copy.pop(key, None)
            result.append(user_copy)
        return result

    def get_public_user_info(self, uid):
        self.users = self.load_users()
        for i, u in enumerate(self.users):
            if u["uid"] == uid:
                user = self.users[i].copy()
                for key in self.keys_to_remove:
                    user.pop(key, None)
                return user
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    def get_user_internal(self, uid):
        self.users = self.load_users()
        for user in self.users:
            if user['uid'] == uid:
                return user
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    def create_user(self, user: UserCreate):
        if  any(u["username"] == user.username for u in self.users):
            raise HTTPException(status_code=400, detail="Username telah digunakan")

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

        try:
            history_file = os.path.join(self.history_path, f"{new_uid}.json")
            with open(history_file, "w") as f:
                json.dump([], f)
        except (PermissionError, TypeError, OSError, json.JSONDecodeError) as e:
            print(f"[Error] Gagal menyimpan history gacha: {e}")

        return self.get_public_user_info(new_uid)

    def add_user_primogems(self, uid:str, primogems: int):
        if primogems < 0:
            raise HTTPException(status_code=400, detail="Primogems tidak boleh negatif" )
        user = self.get_user_internal(uid)
        user["primogems"] += primogems
        self.save_user()

    def update_user(self, uid: str, user: UserCreate):
        for i, u in enumerate(self.users):
            if u["uid"] == uid:
                updated_data = {
                    "uid": uid,
                    "username": user.username,
                    "password": user.password,
                    "primogems": u["primogems"],
                    "pity": u["pity"],
                    "four_star_pity": u["four_star_pity"],
                    "is_rate_on": u["is_rate_on"],
                    "four_star_rate_on": u["four_star_rate_on"],
                    "rarity_weight": u["rarity_weight"],
                }
                self.users[i] = updated_data
                self.save_user()
                return updated_data
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    def save_user_rarity_weight(self, uid: str, rarity_weight: dict):
        expected_keys = {"3-star", "4-star", "5-star"}
        if set(rarity_weight.keys()) != expected_keys:
            raise HTTPException(status_code=400, detail="Rarity weight keys tidak sesuai")

        user = self.get_user_internal(uid)
        user["rarity_weight"] = rarity_weight
        self.save_user()
        return

    def update_user_primogems(self, uid: str):
        user = self.get_user_internal(uid)
        if user["primogems"] >= 160:
            user["primogems"] -= 160
            self.save_user()
        else: 
            raise HTTPException(status_code=400, detail="Primogems tidak cukup")

    def update_user_pity(self, user: dict):
        current_user = self.get_user_internal(user["uid"])
        current_user["pity"] = user["pity"]
        current_user["four_star_pity"] = user["four_star_pity"]
        self.save_user()

    def delete_user(self, uid: str):
        for i, u in enumerate(self.users):
            if u["uid"] == uid:
                history_file = os.path.join(self.history_path, f"{uid}.json")
                try:
                    os.remove(history_file)
                except FileNotFoundError as e:
                    print(f"[Error] Tidak bisa menghapus file: {e}")
                del self.users[i]
                self.save_user()
                return {"message": f"User dengan ID {uid} telah dihapus"}
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    def get_user_history(self, uid: str):
        try:
            history_file = os.path.join(self.history_path, f"{uid}.json")
            with open(history_file, "r") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("History file must contain list")
                return data
        except FileNotFoundError:
            return []
        except (json.JSONDecodeError, ValueError) as e:
            print(f"[Error] Failed to load history for UID {uid}: {e}")
            return []

    def user_authentication(self, username: str, password: str):
        for u in self.users:
            if u["username"] == username:
                user = u
        if user["password"] == password:
            return user
        raise HTTPException(status_code=401, detail="Username atau password salah")
