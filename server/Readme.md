для запуска сервера
python .../detector/server/server.py


для остановки
CTRL + C


при ошибке "Address already in use"
ps -fA | grep python
(выведется что-то типа zmenka   15971 11230  0 14:48 pts/0    00:00:00 python server.py)
kill 11230


для обращения из консоли GET
curl -H "Authorization: Basic YWRtaW46MQ==" -X GET localhost:10001/<URL>


для обращения из консоли POST (/loadjpg передаем файл)
curl -H "Authorization: Basic YWRtaW46MQ==" --data "@.../detector/server/123.jpg" -X POST  localhost:10001/load
