import time
import irsdk

def main():
    ir = irsdk.IRSDK()
    print("⏳ Connexion à iRacing...")
    if not ir.startup():
        print("❌ Impossible de se connecter à iRacing.")
        return

    print("✅ Connecté à iRacing.")
    time.sleep(1)

    player_idx = ir['PlayerCarIdx']
    surfaces = ir['CarIdxTrackSurface']

    print(f"\n🧍‍♂️ Mon carIdx: {player_idx}")
    print(f"🌍 Lecture des surfaces de piste...")

    try:
        drivers = ir['DriverInfo']['Drivers']
        for driver in drivers:
            idx = driver['CarIdx']
            name = driver['UserName']
            if idx == player_idx:
                continue
            surface = surfaces[idx]
            print(f"🚗 {idx:2d} | {name:25s} | Surface: {surface}")
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    main()
