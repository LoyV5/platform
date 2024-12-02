# platform

本地推理只会保存带有结果的txt文件，不保存图片

具体见edge_work.py local_work 95行

云端默认不保存任何结果

具体见rpc_server.py image_handler 97行

0.mp4为测试视频，服务器ip配置文件见config/config.ini

先启动backend_server/rpc_server.py,可使用如下命令：
CUDA_VISIBLE_DEVICES=0 python rpc_server.py

再启动frontend_server/forwarding_server.py,可使用如下命令：
python forwarding_server.py

本地使用python edge_main.py  -f 0.mp4 -i 50可发送测试帧 -i表示帧读取间隔时间,为50ms

结果评估可以用iou_eval.py读取云端和本地的结果，脚本匹配文件名进行比对

#2024.11.18

新增参数-c 是否压缩,默认0,,输入0以png发送,1以jpeg发送

新增参数-t 返回结果类型，默认0,输入0返回txt结果，1返回png图片结果

新增requirement.txt,限anaconda
用conda create --name <env> --file <this file>


待完成：jpeg质量参数未做决策



#2024.11.28

edge和cloud新增参数-wd -ht，可以指定输入图片的宽和高



fforward新增服务器选择策略pick_input,基于输入图片宽和高选择对应服务器



#2024.11.30 

服务器目前可以返回性能数据，保存在output.json和server_info.json中