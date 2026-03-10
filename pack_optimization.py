import simpy
import random
import matplotlib.pyplot as plt
import os
from datetime import datetime

print("Skript startet...")

# ---------------- Ordnerstruktur ----------------

BASE_RESULTS_FOLDER = "simulation_results"
os.makedirs(BASE_RESULTS_FOLDER, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
RUN_FOLDER = os.path.join(BASE_RESULTS_FOLDER, f"run_{timestamp}")
os.makedirs(RUN_FOLDER, exist_ok=True)

print(f"Ergebnisse werden gespeichert in: {RUN_FOLDER}")

# ---------------- Konfiguration ----------------

SIM_CONFIG = {

    "SIM_DAUER_STUNDEN": 8,
    "INTERVALL_ANKUNFT_MINUTEN": 2,

    "NUM_REPLICATIONS": 5,

    "GA_POPULATION_SIZE": 20,
    "GA_NUM_GENERATIONS": 5,
    "GA_MUTATION_RATE": 0.1,

    "ANZAHL_PICKER": 2,
    "PACKSTATION_KAPAZITAET": 1,

    "PICKS_PRO_TYP": {'Small': 2, 'Large': 8},
    "ZEIT_PRO_PICK_EINHEITEN": 1,
    "PACKING_DURATION_EINHEITEN": 3,

    "GESCHWINDIGKEIT_M_PRO_ZEITEINHEIT": 10,

    "DISTANZ_WE_LAGER": 15,
    "DISTANZ_LAGER_PICKZONE": 60,
    "DISTANZ_PICKZONE_PUFFER": 15,
    "DISTANZ_PUFFER_PACK": 15,
    "DISTANZ_PACK_VERSAND": 15,

    "KOSTEN_PRO_PICKER_PRO_SCHICHT": 400,
    "KOSTEN_PRO_PACKSTATION_PRO_SCHICHT": 1000,

    # jetzt klar benannt
    "PENALTY_SCORE_PRO_MINUTE": 5,

    "OPTIMIZATION_TARGET": "total_score",

    "OPTIMIZATION_PARAMETER_RANGES": {

        "ANZAHL_PICKER": {"min": 1, "max": 5, "type": "int"},
        "PACKSTATION_KAPAZITAET": {"min": 1, "max": 3, "type": "int"},
        "GESCHWINDIGKEIT_M_PRO_ZEITEINHEIT": {"min": 5.0, "max": 10.0, "type": "float"},
        "PACKING_DURATION_EINHEITEN": {"min": 1.0, "max": 5.0, "type": "float"}

    }

}

SIM_CONFIG["SIM_ZEIT_TOTAL"] = SIM_CONFIG["SIM_DAUER_STUNDEN"] * 60
SIM_CONFIG["INTERVALL_ANKUNFT_SIM_EINHEITEN"] = SIM_CONFIG["INTERVALL_ANKUNFT_MINUTEN"]

# ---------------- Paketprozess ----------------

def paket(env, name, packstation, picker, stats, paket_typ, config):

    start = env.now

    yield env.timeout(config["DISTANZ_WE_LAGER"]/config["GESCHWINDIGKEIT_M_PRO_ZEITEINHEIT"])
    yield env.timeout(config["DISTANZ_LAGER_PICKZONE"]/config["GESCHWINDIGKEIT_M_PRO_ZEITEINHEIT"])

    picks = config["PICKS_PRO_TYP"][paket_typ]
    picking_time = picks * config["ZEIT_PRO_PICK_EINHEITEN"]

    req_time = env.now

    with picker.request() as req:
        yield req

        wait_picker = env.now - req_time

        yield env.timeout(picking_time)

        stats["picker_work"] += picking_time

    yield env.timeout(config["DISTANZ_PICKZONE_PUFFER"]/config["GESCHWINDIGKEIT_M_PRO_ZEITEINHEIT"])
    yield env.timeout(config["DISTANZ_PUFFER_PACK"]/config["GESCHWINDIGKEIT_M_PRO_ZEITEINHEIT"])

    req_time = env.now

    with packstation.request() as req:
        yield req

        wait_pack = env.now - req_time

        yield env.timeout(config["PACKING_DURATION_EINHEITEN"])

        stats["pack_work"] += config["PACKING_DURATION_EINHEITEN"]

    yield env.timeout(config["DISTANZ_PACK_VERSAND"]/config["GESCHWINDIGKEIT_M_PRO_ZEITEINHEIT"])

    stats["finished"] += 1

    cycle = env.now - start

    stats["details"].append({

        "wait_picker":wait_picker,
        "wait_pack":wait_pack,
        "cycle":cycle

    })


# ---------------- Generator ----------------

def paket_generator(env,config,packstation,picker,stats):

    i=0

    while True:

        i+=1

        typ=random.choices(["Small","Large"],weights=[0.7,0.3])[0]

        env.process(paket(env,f"P{i}",packstation,picker,stats,typ,config))

        yield env.timeout(random.expovariate(1/config["INTERVALL_ANKUNFT_SIM_EINHEITEN"]))


# ---------------- Simulation ----------------

def run_simulation(config):

    env=simpy.Environment()

    packstation=simpy.Resource(env,capacity=config["PACKSTATION_KAPAZITAET"])
    picker=simpy.Resource(env,capacity=config["ANZAHL_PICKER"])

    stats={

        "details":[],
        "finished":0,
        "picker_work":0,
        "pack_work":0

    }

    env.process(paket_generator(env,config,packstation,picker,stats))

    env.run(until=config["SIM_ZEIT_TOTAL"])

    results={}

    if stats["details"]:

        w_picker=[p["wait_picker"] for p in stats["details"]]
        w_pack=[p["wait_pack"] for p in stats["details"]]
        cycle=[p["cycle"] for p in stats["details"]]

        results["avg_wait_picker"]=sum(w_picker)/len(w_picker)
        results["avg_wait_pack"]=sum(w_pack)/len(w_pack)
        results["avg_cycle"]=sum(cycle)/len(cycle)

    else:

        results["avg_wait_picker"]=0
        results["avg_wait_pack"]=0
        results["avg_cycle"]=0

    cost_picker=config["ANZAHL_PICKER"]*config["KOSTEN_PRO_PICKER_PRO_SCHICHT"]
    cost_pack=config["PACKSTATION_KAPAZITAET"]*config["KOSTEN_PRO_PACKSTATION_PRO_SCHICHT"]

    penalty_score = results["avg_cycle"] * config["PENALTY_SCORE_PRO_MINUTE"] * stats["finished"]

    results["total_score"]=cost_picker+cost_pack+penalty_score

    results["finished"]=stats["finished"]

    return results


# ---------------- Genetic Algorithm ----------------

def optimize_factory(config):

    population=[]

    for _ in range(config["GA_POPULATION_SIZE"]):

        ind=config.copy()

        for p,info in config["OPTIMIZATION_PARAMETER_RANGES"].items():

            if info["type"]=="int":
                ind[p]=random.randint(info["min"],info["max"])
            else:
                ind[p]=random.uniform(info["min"],info["max"])

        population.append(ind)

    progress=[]

    best_config=None
    best_score=float("inf")
    best_results=None

    for gen in range(config["GA_NUM_GENERATIONS"]):

        print(f"\nGeneration {gen+1}")

        evaluated=[]

        for ind in population:

            runs=[]

            for _ in range(config["NUM_REPLICATIONS"]):
                runs.append(run_simulation(ind.copy()))

            avg_score=sum(r["total_score"] for r in runs)/len(runs)

            evaluated.append((ind,avg_score,runs[0]))

        evaluated.sort(key=lambda x:x[1])

        best=evaluated[0]

        progress.append({

            "generation":gen+1,
            "best_score":best[1],
            "best_config":best[0],
            "best_results":best[2]

        })

        if best[1]<best_score:

            best_score=best[1]
            best_config=best[0]
            best_results=best[2]

        new_pop=[best[0]]

        while len(new_pop)<config["GA_POPULATION_SIZE"]:

            parent=random.choice(evaluated[:5])[0]

            child=parent.copy()

            for p,info in config["OPTIMIZATION_PARAMETER_RANGES"].items():

                if random.random()<config["GA_MUTATION_RATE"]:

                    if info["type"]=="int":
                        child[p]=random.randint(info["min"],info["max"])
                    else:
                        child[p]=random.uniform(info["min"],info["max"])

            new_pop.append(child)

        population=new_pop

    return best_config,best_results,progress


# ---------------- Hauptprogramm ----------------

if __name__=="__main__":

    best_config,best_results,progress=optimize_factory(SIM_CONFIG)

    print("\nBeste Konfiguration:")

    for k,v in best_config.items():

        if k in SIM_CONFIG["OPTIMIZATION_PARAMETER_RANGES"]:
            print(k,v)

    print("\nErgebnisse:")
    for k,v in best_results.items():
        print(k,v)

    # ---------- Plot 1 ----------

    gens=[p["generation"] for p in progress]
    scores=[p["best_score"] for p in progress]

    plt.figure(figsize=(10,6))
    plt.plot(gens,scores,marker="o")
    plt.title("Optimization Progress")
    plt.xlabel("Generation")
    plt.ylabel("Score")
    plt.grid(True)

    path1=os.path.join(RUN_FOLDER,"optimization_progress.png")
    plt.savefig(path1)
    plt.show()

    # ---------- Plot 2 ----------

    pick=[]
    wait=[]

    for p in progress:

        pick.append(p["best_config"]["ANZAHL_PICKER"])
        wait.append(p["best_results"]["avg_wait_picker"])

    plt.figure(figsize=(10,6))
    plt.scatter(pick,wait)
    plt.xlabel("Number of Pickers")
    plt.ylabel("Average Picker Waiting Time")
    plt.title("Picker vs Waiting Time")
    plt.grid(True)

    path2=os.path.join(RUN_FOLDER,"picker_waiting_time.png")
    plt.savefig(path2)
    plt.show()