import json
import os
import subprocess
import threading
import traceback

_locfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "provider.js")
if os.path.exists(_locfile):
    with open(_locfile, "r", encoding="utf-8") as f:
        _js = f.read()
else:
    _js = "636f6e737420766d203d20726571756972652827766d27293b0a0a70726f636573732e737464696e2e726573756d6528293b0a70726f636573732e737464696e2e736574456e636f64696e6728227574663822293b0a0a66756e6374696f6e206f7574707574287465787429207b0a20202020636f6e736f6c652e6c6f672874657874290a7d0a0a636f6e737420637478203d207b0a202020205f72657475726e3a2066756e6374696f6e20287469642c20727329207b0a20202020202020207273203d207273207c7c207b7d0a20202020202020206f7574707574284a534f4e2e737472696e67696679287b0a20202020202020202020202022746964223a207469642c0a2020202020202020202020202264617461223a2072730a20202020202020207d29293b0a202020207d2c0a202020205f7468726f775f65783a2066756e6374696f6e20287469642c20657829207b0a20202020202020206f7574707574284a534f4e2e737472696e67696679287b0a20202020202020202020202022746964223a207469642c0a2020202020202020202020202265785f6d7367223a2065782e6d6573736167652c0a2020202020202020202020202265785f737461636b223a2065782e737461636b0a20202020202020207d29293b0a202020207d0a7d0a766d2e637265617465436f6e7465787428637478290a0a66756e6374696f6e205f6f6e5f646174612868657829207b0a20202020636f6e737420627566203d204275666665722e66726f6d286865782c202268657822293b0a20202020636f6e7374206a736f6e203d206275662e746f537472696e6728227574663822293b0a20202020636f6e7374206d7367203d204a534f4e2e7061727365286a736f6e290a202020206966202821286d7367202626206d73672e6f70202626206d73672e74696429292072657475726e0a2020202073776974636820286d73672e6f7029207b0a202020202020202063617365202265786563757465223a0a202020202020202020202020747279207b0a20202020202020202020202020202020766d2e72756e496e436f6e74657874286d73672e636f64652c20637478293b0a202020202020202020202020202020206374782e5f72657475726e286d73672e7469642c207b7d293b0a2020202020202020202020207d20636174636820286529207b0a202020202020202020202020202020206374782e5f7468726f775f6578286d73672e7469642c2065290a2020202020202020202020207d0a202020202020202020202020627265616b0a202020202020202063617365202263616c6c223a0a20202020202020206361736520226163616c6c223a0a2020202020202020202020206c657420636f6465203d206e756c6c3b0a202020202020202020202020696620286d73672e6f70203d3d3d20226163616c6c2229207b0a20202020202020202020202020202020636f6465203d20600a2020202020202020202020202020202020202020247b6d73672e666e7d282e2e2e247b6d73672e617267737d292e7468656e2828727329203d3e207b0a2020202020202020202020202020202020202020202020205f72657475726e28247b6d73672e7469647d2c7273293b0a20202020202020202020202020202020202020207d292e63617463682828657829203d3e207b0a2020202020202020202020202020202020202020202020205f7468726f775f657828247b6d73672e7469647d2c6578293b0a20202020202020202020202020202020202020207d290a20202020202020202020202020202020603b0a2020202020202020202020207d20656c7365207b0a20202020202020202020202020202020636f6465203d20600a20202020202020202020202020202020202020207472797b0a2020202020202020202020202020202020202020202020205f72657475726e28247b6d73672e7469647d2c247b6d73672e666e7d282e2e2e247b6d73672e617267737d29293b0a20202020202020202020202020202020202020207d20636174636828657829207b0a2020202020202020202020202020202020202020202020205f7468726f775f657828247b6d73672e7469647d2c6578293b0a20202020202020202020202020202020202020207d0a20202020202020202020202020202020603b0a2020202020202020202020207d0a202020202020202020202020747279207b0a20202020202020202020202020202020766d2e72756e496e436f6e7465787428636f64652c20637478293b0a2020202020202020202020207d20636174636820286529207b0a202020202020202020202020202020206374782e5f7468726f775f6578286d73672e7469642c2065290a2020202020202020202020207d0a202020202020202020202020627265616b0a202020207d0a7d0a0a70726f636573732e737464696e2e6f6e282264617461222c202868657829203d3e207b0a20202020747279207b0a20202020202020205f6f6e5f6461746128686578290a202020207d20636174636820286529207b0a20202020202020206374782e5f7468726f775f6578282d312c206578290a202020207d0a7d293b0a0a6f757470757428226e6f646534707920697320726561647922290a"
    _js = bytes.fromhex(_js).decode("utf-8")


def _get_proc(node_path=None, cwd=None, cmd=None):
    if node_path is None:
        node_path = "node"
    if cmd is None:
        cmd = []
    p = subprocess.Popen(
        [node_path, "-e", _js] + cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        cwd=cwd
    )
    return p


class JsEx(Exception):
    def __init__(self, msg, stack):
        self.msg = msg
        self.stack = stack

    def __str__(self):
        return self.msg + "\n" + self.stack


class JsRunner:
    def __init__(self, node_path=None, cwd=None, cmd=None):
        self._proc = _get_proc(node_path, cwd, cmd)
        self._lock = threading.Lock()
        self._ret = None
        self._tid = 0
        self._is_running = True
        self._ev = threading.Event()
        self._ev.clear()
        threading.Thread(target=self._output, daemon=True).start()
        self._ev.wait()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def close(self):
        if self._proc is not None:
            self._proc.terminate()
            self._proc.wait()
            self._proc = None
        self._is_running = False

    def _output(self):
        try:
            while self._is_running:
                line = self._proc.stdout.readline()
                if line == '' and self._proc.poll() is not None:
                    break
                line = line.strip()
                if line == "node4py is ready":
                    self._ev.set()
                if line and line.startswith("{"):
                    msg = json.loads(line)
                    if msg and msg.get("tid") == self._tid:
                        ex_msg = msg.get("ex_msg")
                        if ex_msg is not None:
                            self._ret = JsEx(ex_msg, msg.get("ex_stack"))
                        else:
                            self._ret = msg.get("data")
                        self._ev.set()
                    elif msg.get("tid") == -1:
                        self._ret = JsEx(msg.get("ex_msg"), msg.get("ex_stack"))
                        self._ev.set()
        except:
            if self._is_running:
                traceback.print_exc()
        finally:
            self.close()

    def execute(self, code):
        with self._lock:
            self._tid += 1
            msg = json.dumps({
                "op": "execute",
                "tid": self._tid,
                "code": code
            })
            msg = msg.encode("utf-8").hex()
            self._proc.stdin.write(msg)
            self._proc.stdin.flush()
            self._ev.clear()
            self._ev.wait()
            if isinstance(self._ret, JsEx):
                raise self._ret

    def __call(self, call_name, func, *args):
        with self._lock:
            self._tid += 1
            msg = json.dumps({
                "op": call_name,
                "tid": self._tid,
                "fn": func,
                "args": json.dumps(args)
            })
            msg = msg.encode("utf-8").hex()
            self._proc.stdin.write(msg)
            self._proc.stdin.flush()
            self._ev.clear()
            self._ev.wait()
            if isinstance(self._ret, JsEx):
                raise self._ret
            return self._ret

    def call(self, func, *args):
        return self.__call("call", func, *args)

    def acall(self, func, *args):
        return self.__call("acall", func, *args)


node = r"D:\Code\bigo\xlib\Lib\site-packages\playwright\driver\node.exe"

if __name__ == "__main__":
    print()
    if os.path.exists(_locfile):
        with open(_locfile, "r") as f:
            print(f.read().encode("utf-8").hex())

    with JsRunner(node) as r:
        r.execute('''
            function show(t_bool,t_int,t_str,t_dict,t_list){
                let rs = [
                    "sync call",
                    `t_bool=${t_bool}`,
                    `t_int=${t_int}`,
                    `t_str=${t_str}`,
                    `t_dict=${JSON.stringify(t_dict)}`,
                    `t_list=${JSON.stringify(t_list)}`,
                ]
                return rs.join("\\n");
            }
            
            async function a_show(t_bool,t_int,t_str,t_dict,t_list){
                let rs = [
                    "async call",
                    `t_bool=${t_bool}`,
                    `t_int=${t_int}`,
                    `t_str=${t_str}`,
                    `t_dict=${JSON.stringify(t_dict)}`,
                    `t_list=${JSON.stringify(t_list)}`,
                ]
                return rs.join("\\n");
            }
        ''')
        while True:
            tx = input("Press key")
            if tx == "0":
                break
            if tx == "1":
                print(r.call("show",
                             True,
                             111,
                             "string",
                             {"dictkey": "dictvalue"},
                             [111, "str", {"dk": "dv"}, [1, 2, 3]]))
            if tx == "2":
                print(r.acall("a_show",
                              False,
                              222,
                              "string",
                              {"dictkey": "dictvalue"},
                              [222, "str", {"dk": "dv"}, [4, 5, 6]]))
