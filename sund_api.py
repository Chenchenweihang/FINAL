import requests


def get_sund_music():
    url = "https://api.acedata.cloud/suno/audios"

    headers = {
        "accept": "application/json",
        "authorization": "Bearer d2a86fcd95c24ae68f2bf4a07cb87f09",
        "content-type": "application/json"
    }

    payload = {
        "action": "generate",
        # 歌曲的提示词
        "prompt": "A song for Christmas",
        "model": "chirp-v3-5",
        # 是否使用自定义歌词生成歌曲
        "custom": False,
        # 是否使用歌词
        "instrumental": True,
        "title": "ai_music",
        # 歌曲的风格
        "style": "happy"
    }

    response = requests.post(url, json=payload, headers=headers)
    # demo of response.json()
    # {
    #   "data": [
    #     {
    #       "id": "75d8e08f-b25f-450e-9496-7b52e393098b",
    #       "lyric": "[Verse]\nSleigh bells ringin', choirs singin'\nSnowflakes fallin', presents glistenin' (glistenin')\nIn the air, there's a feeling of joy\nSpreadin' love to every girl and boy\n[Verse 2]\nCandles glowin', fire cracklin'\nStockings hangin', children wrappin'\nWith a smile, they unwrap their surprise\nIn their hearts, the magic never dies\n[Chorus]\nJingle all the way (jingle all the way)\nIn the winter wonderland, we play (oh-oh)\nHear the carols echo through the night (echo through the night)\nMerry Christmas, oh what a delight (oh-oh-oh)",
    #       "model": "chirp-v3",
    #       "style": "pop upbeat",
    #       "title": "Jingle All the Way",
    #       "prompt": "a christmas song",
    #       "audio_url": "https://audiopipe.suno.ai/?item_id=75d8e08f-b25f-450e-9496-7b52e393098b",
    #       "image_url": "https://cdn1.suno.ai/image_75d8e08f-b25f-450e-9496-7b52e393098b.png",
    #       "video_url": "",
    #       "created_at": "2024-04-03T11:54:30.424Z"
    #     },
    #     {
    #       "id": "e639fefd-bbd3-4858-b16d-45e7d4aa9313",
    #       "lyric": "[Verse]\nSleigh bells ringin', choirs singin'\nSnowflakes fallin', presents glistenin' (glistenin')\nIn the air, there's a feeling of joy\nSpreadin' love to every girl and boy\n[Verse 2]\nCandles glowin', fire cracklin'\nStockings hangin', children wrappin'\nWith a smile, they unwrap their surprise\nIn their hearts, the magic never dies\n[Chorus]\nJingle all the way (jingle all the way)\nIn the winter wonderland, we play (oh-oh)\nHear the carols echo through the night (echo through the night)\nMerry Christmas, oh what a delight (oh-oh-oh)",
    #       "model": "chirp-v3",
    #       "style": "pop upbeat",
    #       "title": "Jingle All the Way",
    #       "prompt": "a christmas song",
    #       "audio_url": "https://audiopipe.suno.ai/?item_id=e639fefd-bbd3-4858-b16d-45e7d4aa9313",
    #       "image_url": "https://cdn1.suno.ai/image_e639fefd-bbd3-4858-b16d-45e7d4aa9313.png",
    #       "video_url": "",
    #       "created_at": "2024-04-03T11:54:30.424Z"
    #     }
    #   ],
    #   "success": true
    # }

    # 保存音频的地址
    audio_url = response.json()['data'][0]['audio_url']
    print(audio_url)
    return audio_url
