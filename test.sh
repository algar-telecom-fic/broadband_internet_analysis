i=0
while [ $i -lt 360 ]; do
  python3.6 /home/gardusi/github/broadband_internet_analysis/gpon_traffic/main.py
  python3.6 /home/gardusi/github/broadband_internet_analysis/hfc/main.py
  python3.6 /home/gardusi/github/broadband_internet_analysis/xdsl/main.py
  let i+=1
done