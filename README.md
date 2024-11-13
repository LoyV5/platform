# platform

本地推理只会保存带有结果的txt文件，不保存图片

具体见edge_work.py local_work 95行



云端默认也只保存带有结果的txt文件

具体见rpc_server.py image_handler 97行



0.mp4为测试视频，配置文件见config/config.ini



先启动rpc_server.py，再启动forwarding_server.py

本地使用python edge_main.py  -f 0.mp4 -i 50可发送测试帧



结果评估可以用iou_eval.py读取云端和本地的结果，脚本匹配文件名进行比对