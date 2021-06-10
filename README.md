# frame_overlaying
 利用动目标检测制作连续动作帧叠加作品

从一段视频中提取动态目标，帧叠加形成一张图片，展示运动轨迹。运动目标检测方法：帧的灰度图和背景灰度图作差，二值处理形成蒙版，再形态学处理（开环去噪点，闭环补空隙，可以调整核大小kopen kclose）. 所以录制视频背景不能动，需要固定住相机。

## 作品展示：

![image](https://user-images.githubusercontent.com/69345371/121506416-4293b600-ca16-11eb-8af9-7485cf28e062.png)

![image](https://user-images.githubusercontent.com/69345371/121506464-4fb0a500-ca16-11eb-93d8-bc2856d02c06.png)

![image](https://user-images.githubusercontent.com/69345371/121506503-5a6b3a00-ca16-11eb-90cc-932f638cb9bd.png)
