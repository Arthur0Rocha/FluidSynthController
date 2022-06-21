import subprocess
import os

VORTEX_NAME = "Vortex Wireless 2"
KROME_NAME = "KROME"
ARTHUR_SEQ_NAME = "Arthur SEQ"
FSYNTH_CONTROLLER_NAME = 'FSynth-Controller'
QSYNTH_NAME = "FLUID Synth (qsynth)"
FLUID_SYNTH_NAME = "FLUID Synth (ARX)"
M_VAVE_NAME = "SINCO"

SYSTEM_NAME = "System"
MIDI_THROUGH_NAME = "Midi Through"

def read_clients():
    clients = []
    ports = {}
    connections = []

    s = subprocess.check_output("aconnect -l", shell=True).decode("utf-8")
    
    for line in s.split('client')[1:]:
        line = line.strip().splitlines()
        code, name = line[0].split(':')
        code = int(code)
        name = name.split('\'')[1]
        clients.append(name)
        ports[name] = code
        ports[code] = name
        line = line[1:]
        while len(line) > 0:
            port = int(line[0].strip().split(' ')[0])
            line = line[1:]
            while len(line) > 0:
                if 'Connecting To' in line[0]:
                    conn = int(line[0].split(':')[1].strip())
                    connections = list(set(connections + [(code, conn)]))
                    line = line[1:]
                    pass
                elif 'Connected From' in line[0]:
                    conn = int(line[0].split(':')[1].strip())
                    connections = list(set(connections + [(conn, code)]))
                    line = line[1:]
                    pass
                else:
                    break
                
    return clients, ports, connections

def disconnect_all():
    os.system("aconnect -x")

def make_connections(clients, ports, connections):
    if VORTEX_NAME in clients \
        and FSYNTH_CONTROLLER_NAME in clients \
            and (ports[VORTEX_NAME], ports[FSYNTH_CONTROLLER_NAME]) not in connections:
        os.system(f"aconnect {ports[VORTEX_NAME]} {ports[FSYNTH_CONTROLLER_NAME]} > log")

    if FSYNTH_CONTROLLER_NAME in clients \
        and QSYNTH_NAME in clients \
            and (ports[FSYNTH_CONTROLLER_NAME], ports[QSYNTH_NAME]) not in connections:
        os.system(f"aconnect {ports[FSYNTH_CONTROLLER_NAME]}:1 {ports[QSYNTH_NAME]} > log")

    if FSYNTH_CONTROLLER_NAME in clients \
        and FLUID_SYNTH_NAME in clients \
            and (ports[FSYNTH_CONTROLLER_NAME], ports[FLUID_SYNTH_NAME]) not in connections:
        os.system(f"aconnect {ports[FSYNTH_CONTROLLER_NAME]}:1 {ports[FLUID_SYNTH_NAME]} > log")

    # if M_VAVE_NAME in clients \
    #     and MIDI_THROUGH_NAME in clients \
    #         and (ports[M_VAVE_NAME], ports[MIDI_THROUGH_NAME]) not in connections:
    #     os.system(f"aconnect {ports[M_VAVE_NAME]} {ports[MIDI_THROUGH_NAME]} > log")

    if M_VAVE_NAME in clients \
        and FSYNTH_CONTROLLER_NAME in clients \
            and (ports[M_VAVE_NAME], ports[FSYNTH_CONTROLLER_NAME]) not in connections:
        os.system(f"aconnect {ports[M_VAVE_NAME]} {ports[FSYNTH_CONTROLLER_NAME]} > log")

def run():
    clients, ports, connections = read_clients()
    make_connections(clients, ports, connections)
    return clients, ports, connections

if __name__ == "__main__":
    run()


