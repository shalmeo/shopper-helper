def get_profile_text(user_id: int, user_tracks: int) -> list[str]: 
    text = [
        f'<b>Ваш ID: <code>{user_id}</code></b>\n\n'
        f'🔎 Информация\n'
        f'└» Количество товаров: <code>{user_tracks}</code>'
    ]
    
    return text