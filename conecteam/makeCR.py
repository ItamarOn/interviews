def update_users_groups_v1(group_id: int, filter: str) -> None:
    for user in UsersDAL.fetch():
        user_group = UserGroupDAL.fetch(user.id, group_id)
        if does_user_pass_filter(filter, user):
            # be in UserGroupModel
            if not user_group:
                UserGroupDAL.insert(user.id, group_id)
        else:
            # dont be in UserGroupModel
            if user_group:
                UserGroupDAL.delete(user_group)

class UserModel:
    id: int
    name: str

class UserGroupModel:
    user_id: int
    group_id: int

def does_user_pass_filter(filter: str, user: UserModel) -> bool:
    pass

class UsersDAL:
    def fetch() -> list[UserModel]:
        pass


class UserGroupDAL:
    def fetch(user_id: int, group_id: int) -> UserGroupModel:
        pass

    def insert(user_id: int, group_id: int) -> None:
        pass

    def delete(user_group_data: UserGroupModel) -> None:
        pass