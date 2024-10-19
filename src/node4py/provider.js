const vm = require('vm');

process.stdin.resume();
process.stdin.setEncoding("utf8");

function output(text) {
    console.log(text)
}

const ctx = {
    _return: function (tid, rs) {
        rs = rs || {}
        output(JSON.stringify({
            "tid": tid,
            "data": rs
        }));
    },
    _throw_ex: function (tid, ex) {
        output(JSON.stringify({
            "tid": tid,
            "ex_msg": ex.message,
            "ex_stack": ex.stack
        }));
    }
}
vm.createContext(ctx)

function _on_data(hex) {
    const buf = Buffer.from(hex, "hex");
    const json = buf.toString("utf8");
    const msg = JSON.parse(json)
    if (!(msg && msg.op && msg.tid)) return
    switch (msg.op) {
        case "execute":
            try {
                vm.runInContext(msg.code, ctx);
                ctx._return(msg.tid, {});
            } catch (e) {
                ctx._throw_ex(msg.tid, e)
            }
            break
        case "call":
        case "acall":
            let code = null;
            if (msg.op === "acall") {
                code = `
                    ${msg.fn}(...${msg.args}).then((rs) => {
                        _return(${msg.tid},rs);
                    }).catch((ex) => {
                        _throw_ex(${msg.tid},ex);
                    })
                `;
            } else {
                code = `
                    try{
                        _return(${msg.tid},${msg.fn}(...${msg.args}));
                    } catch(ex) {
                        _throw_ex(${msg.tid},ex);
                    }
                `;
            }
            try {
                vm.runInContext(code, ctx);
            } catch (e) {
                ctx._throw_ex(msg.tid, e)
            }
            break
    }
}

process.stdin.on("data", (hex) => {
    try {
        _on_data(hex)
    } catch (e) {
        ctx._throw_ex(-1, ex)
    }
});

output("node4py is ready")
