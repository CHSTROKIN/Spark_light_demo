- ## 环境准备

  - 视情况通过requirement_pip或者requirement_conda安装环境
    - 已经安装python的通过`pip install -r requirements.txt` 安装依赖
  - 本程序不包含任何模型训练，部署。预测功能通过mediapipe实现
  - 遇到bug
    - google/百度 stackoverflow
  - 没解决
    - email: 1844697834@qq.com
    - 找老师联系戚皓天（本人姓名）同学


  ## 数据准备

  - 爬虫。另外，不构成建议，**本人不对任何爬虫行为负责**
  - 如果不想从头开始爬图片，在data文件夹内有训练图片。数量有限。
  - data

  ```
  data/
  └── five/
  	└──153710 WIN_20220718_21_36_38_Pro (2).jpg
  	└──154524 WIN_20220718_21_36_38_Pro.jpg
  	└──152155 WIN_20220718_21_36_39_Pro.jpg
  	└──153736 WIN_20220718_21_36_40_Pro.jpg
  	└──153997 WIN_20220718_21_36_41_Pro (2).jpg
  	└──153605 WIN_20220718_21_36_41_Pro.jpg
  └── ture_data.zip
  
  ```

  ##### 

  ## 用法：直接在子文件内运行

  任务的参考实现（石头剪子布没有参考实现）
  石头剪子布

  ```python
  python spark_light\paper_scissor_stone\paper_scissor_stone.py
  ```

  虚拟画板

  ```
  python spark_light\virtue_canvas\hand_drawing_参考实现.py
  ```

  虚拟键盘

  ```
  python spark_light\virtue_keyboard\hand_keyboard_参考实现.py
  ```

  程序流程图在每个文件夹里, 格式为 xxx.drawio


  ## 挑战任务（选做，PPT里没有）

- **剪刀石头布**

  - 1：实现抢先出手判断
  - 2：通过socket实现局域网PVP
    - 注意关闭防火墙，并打开端口

- **虚拟画板**

  - 1：贝塞尔曲线功能
  - 2：导出图片，并实现手写数字识别
    - 提示：
      - 记录坐标点
      - 画到空白图片上
      - 准备好用**mnist**数据集（请自行google/百度）训练的模型
      - 模型预测

- **虚拟键盘**

  - 1：实现虚拟鼠标
    - 提示：
      - 记录坐标点
      - 画到桌面实时截图上
      - 模拟鼠标输出

  