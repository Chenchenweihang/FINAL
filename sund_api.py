import requests
from click import prompt


def get_sund_music(text,style):
    url = "https://api.acedata.cloud/suno/audios"

    headers = {
        "accept": "application/json",
        "authorization": "Bearer d2a86fcd95c24ae68f2bf4a07cb87f09",
        "content-type": "application/json"
    }

    payload = {
        "action": "generate",
        # 歌曲的提示词
        # "prompt": "A song for Christmas",
        "prompt":text,
        "model": "chirp-v3-5",
        # 是否使用自定义歌词生成歌曲
        "custom": False,
        # 是否使用歌词
        "instrumental": True,
        "title": "ai_music",
        # 歌曲的风格
        # "style": "happy"
        "style":style
    }

    response = requests.post(url, json=payload, headers=headers, verify=False)
    # /**
    # demo of response.json()
    # **/
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

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # 检查是否有请求错误
        response_json = response.json()

        if response_json.get('success'):
            audio_url = response_json['data'][0]['audio_url']
            print("Generated audio URL:", audio_url)
            return audio_url
        else:
            print("Failed to generate music:", response_json)
            return None

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None
    except KeyError:
        print("Unexpected response format:", response.text)
        return None

    # 保存音频的地址
    audio_url = response.json()['data'][0]['audio_url']
    print(audio_url)
    return audio_url
