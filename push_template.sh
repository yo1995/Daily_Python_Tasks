Cur_Dir=$(pwd)
echo $Cur_Dir
cd $Cur_Dir

git status
git add .
read -p "当前提交版本：" version
read -p "键入今日提交次序：" order
read -p "提交原因：" reason
git commit -m "Ver $version at $(date +%Y%m%d) $order commit for $reason"
git push
read -s -n1 -p "推出完毕，任意键退出！" qu
