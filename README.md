# node4py
Using Node.js to execute JavaScript in Python

Only one file

Sync call and async call

Keep the Node.js process running

# demo
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
        print(r.call("show",
                     True,
                     111,
                     "string",
                     {"dictkey": "dictvalue"},
                     [111, "str", {"dk": "dv"}, [1, 2, 3]]))
        print(r.acall("a_show",
                      False,
                      222,
                      "string",
                      {"dictkey": "dictvalue"},
                      [222, "str", {"dk": "dv"}, [4, 5, 6]]))