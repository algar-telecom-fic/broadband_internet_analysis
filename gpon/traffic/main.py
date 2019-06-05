from gpon_traffic import GPON

def main():
  gpon = GPON()
  gpon.read_ports()
  gpon.read_traffic()
  gpon.build_documents()
  gpon.insert_documents()


if __name__ == "__main__":
    main()
