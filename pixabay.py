import requests
from wxauto import WeChat
import os
def get_pixabay_images(api_key:str,query: str, per_page: int = 60) -> list:
    url=f"https://pixabay.com/api/?key={api_key}&q={query}&image_type=photo&per_page={per_page}"
    response=requests.get(url)
    pictures=response.json()["hits"]
    for picture in pictures:
        picture_url=picture["largeImageURL"]
        #下载图片
        image_response = requests.get(picture_url)
        if image_response.status_code == 200:
            pic_path = f"images/{picture['id']}.jpg"
            #拼接图片的绝对路径
            ab_pic_path = os.path.abspath(pic_path)

            with open(pic_path, 'wb') as f:
                f.write(image_response.content)
            return ab_pic_path
           # try:
            #    wx=WeChat()
             #   wx.SendFiles(ab_pic_path, "小池")
           # except Exception as e:
            #    print(str(e))
        else:
            print(f"Failed to download image {picture['id']}")
if __name__ == '__main__':
    url=get_pixabay_images(api_key="47054162-b71e0d9aadb68e45d834827c7", query="cat", per_page=10)
    print(url)