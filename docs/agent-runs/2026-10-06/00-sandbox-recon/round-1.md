# 本地沙箱侦察报告

## 当前阶段 / Current phase
本地离线侦察已完成。

## 已验证事实 / Verified facts
- A–G 所列命令均已执行。
- 本次所需命令均存在；没有需要标注“未安装”的项目。
- 原始输出共 242 行、46,732 字节。
- SHA-256：`fe384f20c7b66cc6bc6b165729634f0c1a02920c684941dfe083a5086e71c6bb`

## 关键证据 / Key evidence

以下为完整原始命令输出，未截断：

```text
===== A. 系统与身份 =====
$ whoami; id; uname -a; cat /etc/os-release 2>/dev/null | head -3; cat /proc/1/cgroup 2>/dev/null
user
uid
Linux e2b.local 6.1.158+ #1 SMP PREEMPT_DYNAMIC Fri Jul 17 14:31:34 UTC 2026 x86_64 GNU/Linux
PRETTY_NAME
NAME
VERSION_ID
0::/init.scope

===== B. 环境变量（全量） =====
$ env | sort
E2B_EVENTS_ADDRESS
E2B_SANDBOX
E2B_SANDBOX_ID
E2B_TEMPLATE_ID
HOME
LOGNAME
PATH
PWD
SHELL
SHLVL
USER
_

===== C. 网络 =====
$ cat /etc/hosts; cat /etc/resolv.conf; ip addr 2>/dev/null || ifconfig 2>/dev/null; ip route 2>/dev/null; ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null
127.0.0.1        localhost
::1              localhost ip6-localhost ip6-loopback
fe00::           ip6-localnet
ff00::           ip6-mcastprefix
ff02::1          ip6-allnodes
ff02::2          ip6-allrouters
127.0.1.1        e2b.local
192.0.2.1        events.e2b.local
nameserver 8.8.8.81: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host proto kernel_lo 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 02:fc:00:00:00:05 brd ff:ff:ff:ff:ff:ff
    inet 169.254.0.21/30 brd 169.254.0.23 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::fc:ff:fe00:5/64 scope link proto kernel_ll 
       valid_lft forever preferred_lft forever
default via 169.254.0.22 dev eth0 
169.254.0.20/30 dev eth0 proto kernel scope link src 169.254.0.21 
State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess
LISTEN 0      100        127.0.0.1:35769      0.0.0.0:*          
LISTEN 0      5       169.254.0.21:47945      0.0.0.0:*          
LISTEN 0      5       169.254.0.21:34675      0.0.0.0:*          
LISTEN 0      4096         0.0.0.0:111        0.0.0.0:*          
LISTEN 0      5       169.254.0.21:35769      0.0.0.0:*          
LISTEN 0      100        127.0.0.1:47945      0.0.0.0:*          
LISTEN 0      100        127.0.0.1:34675      0.0.0.0:*          
LISTEN 0      128        127.0.0.1:8888       0.0.0.0:*          
LISTEN 0      5       169.254.0.21:8888       0.0.0.0:*          
LISTEN 0      100        127.0.0.1:44461      0.0.0.0:*          
LISTEN 0      5       169.254.0.21:35105      0.0.0.0:*          
LISTEN 0      100        127.0.0.1:39379      0.0.0.0:*          
LISTEN 0      100        127.0.0.1:41435      0.0.0.0:*          
LISTEN 0      100        127.0.0.1:43501      0.0.0.0:*          
LISTEN 0      100        127.0.0.1:35105      0.0.0.0:*          
LISTEN 0      5       169.254.0.21:44461      0.0.0.0:*          
LISTEN 0      5       169.254.0.21:39379      0.0.0.0:*          
LISTEN 0      5       169.254.0.21:41435      0.0.0.0:*          
LISTEN 0      5       169.254.0.21:43501      0.0.0.0:*          
LISTEN 0      5       169.254.0.21:60465      0.0.0.0:*          
LISTEN 0      5       169.254.0.21:53335      0.0.0.0:*          
LISTEN 0      5       169.254.0.21:60493      0.0.0.0:*          
LISTEN 0      2048         0.0.0.0:49999      0.0.0.0:*          
LISTEN 0      100        127.0.0.1:60465      0.0.0.0:*          
LISTEN 0      100        127.0.0.1:60493      0.0.0.0:*          
LISTEN 0      100        127.0.0.1:53335      0.0.0.0:*          
LISTEN 0      4096            [::]:111           [::]:*          
LISTEN 0      4096               *:22               *:*          
LISTEN 0      128            [::1]:8888          [::]:*          
LISTEN 0      4096               *:49983            *:*          

===== D. 进程 =====
$ ps aux 2>/dev/null
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.7  0.6  23024 13988 ?        Ss   16:28   0:00 /sbin/init
root           2  0.0  0.0      0     0 ?        S    16:28   0:00 [kthreadd]
root           3  0.0  0.0      0     0 ?        I<   16:28   0:00 [rcu_gp]
root           4  0.0  0.0      0     0 ?        I<   16:28   0:00 [rcu_par_gp]
root           5  0.0  0.0      0     0 ?        I<   16:28   0:00 [slub_flushwq]
root           6  0.0  0.0      0     0 ?        I<   16:28   0:00 [netns]
root           7  0.0  0.0      0     0 ?        I    16:28   0:00 [kworker/0:0-events]
root           8  0.0  0.0      0     0 ?        I<   16:28   0:00 [kworker/0:0H-events_highpri]
root           9  0.4  0.0      0     0 ?        I    16:28   0:00 [kworker/u4:0-ext4-rsv-conversion]
root          10  0.0  0.0      0     0 ?        I<   16:28   0:00 [mm_percpu_wq]
root          11  0.0  0.0      0     0 ?        I    16:28   0:00 [rcu_tasks_kthread]
root          12  0.0  0.0      0     0 ?        I    16:28   0:00 [rcu_tasks_rude_kthread]
root          13  0.0  0.0      0     0 ?        I    16:28   0:00 [rcu_tasks_trace_kthread]
root          14  0.0  0.0      0     0 ?        S    16:28   0:00 [ksoftirqd/0]
root          15  0.0  0.0      0     0 ?        I    16:28   0:00 [rcu_preempt]
root          16  0.0  0.0      0     0 ?        S    16:28   0:00 [migration/0]
root          17  0.0  0.0      0     0 ?        I    16:28   0:00 [kworker/0:1-cgroup_offline]
root          18  0.0  0.0      0     0 ?        S    16:28   0:00 [cpuhp/0]
root          19  0.0  0.0      0     0 ?        S    16:28   0:00 [cpuhp/1]
root          20  0.0  0.0      0     0 ?        S    16:28   0:00 [migration/1]
root          21  0.0  0.0      0     0 ?        S    16:28   0:00 [ksoftirqd/1]
root          22  0.0  0.0      0     0 ?        I    16:28   0:00 [kworker/1:0-events]
root          23  0.0  0.0      0     0 ?        I<   16:28   0:00 [kworker/1:0H-events_highpri]
root          25  0.1  0.0      0     0 ?        I    16:28   0:00 [kworker/u4:1-ext4-rsv-conversion]
root          26  0.0  0.0      0     0 ?        S    16:28   0:00 [kdevtmpfs]
root          27  0.0  0.0      0     0 ?        I<   16:28   0:00 [inet_frag_wq]
root          28  0.0  0.0      0     0 ?        S    16:28   0:00 [kauditd]
root          29  0.0  0.0      0     0 ?        S    16:28   0:00 [khungtaskd]
root          30  0.0  0.0      0     0 ?        S    16:28   0:00 [oom_reaper]
root          31  0.0  0.0      0     0 ?        I    16:28   0:00 [kworker/u4:2-writeback]
root          32  0.0  0.0      0     0 ?        I<   16:28   0:00 [writeback]
root          33  0.0  0.0      0     0 ?        S    16:28   0:00 [kcompactd0]
root          34  0.0  0.0      0     0 ?        SN   16:28   0:00 [ksmd]
root          35  0.0  0.0      0     0 ?        SN   16:28   0:00 [khugepaged]
root          36  0.0  0.0      0     0 ?        I<   16:28   0:00 [kintegrityd]
root          37  0.0  0.0      0     0 ?        I<   16:28   0:00 [kblockd]
root          38  0.0  0.0      0     0 ?        I<   16:28   0:00 [blkcg_punt_bio]
root          39  0.0  0.0      0     0 ?        I    16:28   0:00 [kworker/1:1-cgroup_release]
root          40  0.0  0.0      0     0 ?        S    16:28   0:00 [watchdogd]
root          41  0.0  0.0      0     0 ?        I<   16:28   0:00 [rpciod]
root          42  0.0  0.0      0     0 ?        I<   16:28   0:00 [xprtiod]
root          43  0.0  0.0      0     0 ?        I    16:28   0:00 [kworker/u4:3-flush-254:0]
root          47  0.0  0.0      0     0 ?        I    16:28   0:00 [kworker/u4:4-writeback]
root          53  0.0  0.0      0     0 ?        I<   16:28   0:00 [kworker/1:1H-kblockd]
root          68  0.0  0.0      0     0 ?        S    16:28   0:00 [kswapd0]
root          71  0.0  0.0      0     0 ?        I<   16:28   0:00 [nfsiod]
root          72  0.0  0.0      0     0 ?        I<   16:28   0:00 [kworker/0:1H-kblockd]
root          74  0.0  0.0      0     0 ?        I<   16:28   0:00 [xfsalloc]
root          76  0.0  0.0      0     0 ?        I<   16:28   0:00 [xfs_mru_cache]
root          79  0.0  0.0      0     0 ?        I<   16:28   0:00 [kthrotld]
root          82  0.0  0.0      0     0 ?        I    16:28   0:00 [kworker/0:2-events]
root          84  0.0  0.0      0     0 ?        S    16:28   0:00 [irq/24-ACPI:Ged]
root         117  0.0  0.0      0     0 ?        S    16:28   0:00 [hwrng]
root         141  0.0  0.0      0     0 ?        I<   16:28   0:00 [iscsi_conn_clea]
root         165  0.0  0.0      0     0 ?        I<   16:28   0:00 [mld]
root         166  0.0  0.0      0     0 ?        I<   16:28   0:00 [ipv6_addrconf]
root         173  0.0  0.0   1004     4 ?        S    16:28   0:00 bpfilter_umh
root         174  0.0  0.0      0     0 ?        I<   16:28   0:00 [kstrp]
root         179  0.0  0.0      0     0 ?        I<   16:28   0:00 [zswap-shrink]
root         180  0.0  0.0      0     0 ?        I<   16:28   0:00 [kworker/u5:0]
root         257  0.1  0.0      0     0 ?        S    16:28   0:00 [jbd2/vda-8]
root         258  0.0  0.0      0     0 ?        I<   16:28   0:00 [ext4-rsv-conver]
root         290  0.2  0.4  29440  8948 ?        Ss   16:28   0:00 /usr/lib/systemd/systemd-journald
root         300  0.0  0.0      0     0 ?        I    16:28   0:00 [kworker/1:2-events]
root         305  0.0  0.0      0     0 ?        I    16:28   0:00 [kworker/1:3-mm_percpu_wq]
systemd+     308  0.1  0.5  20752 10316 ?        Ss   16:28   0:00 /usr/lib/systemd/systemd-networkd
_rpc         336  0.0  0.0   6560  1992 ?        Ss   16:28   0:00 /usr/sbin/rpcbind -f -w
message+     340  0.0  0.1   6828  3624 ?        Ss   16:28   0:00 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only
root         341  0.1  0.3  18384  7176 ?        Ss   16:28   0:00 /usr/lib/systemd/systemd-logind
root         359  1.6  1.1 1272548 23448 ?       S<Lsl 16:28   0:00 /usr/bin/envd
root         387  0.0  0.3  11760  7732 ?        Ss   16:28   0:00 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
root         392  0.0  0.0      0     0 ?        I    16:28   0:00 [kworker/0:3-events]
root         393  0.0  0.0      0     0 ?        I    16:28   0:00 [kworker/0:4-events]
root         421  0.0  0.0   5168  1584 tty1     Ss+  16:28   0:00 /sbin/agetty -o -- \u --noreset --noclear - linux
root         422  0.0  0.0   5248   204 ?        Ss   16:28   0:00 /usr/sbin/blkmapd
root         437  8.1  4.8 256896 99052 ?        Ssl  16:28   0:01 /usr/local/bin/python3.13 /usr/local/bin/jupyter-server --IdentityProvider.token=[REDACTED:last4=(empty)]
root         463  3.0  3.2 371148 66132 ?        Ssl  16:28   0:00 /root/.server/.venv/bin/python /root/.server/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 49999 --workers 1 --no-access-log --no-use-colors --timeout-keep-alive 640
root         470  0.0  0.1  11716  3024 ?        S<   16:28   0:00 socat -d -d -d TCP4-LISTEN:8888,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:8888
root         475  2.5  3.6 771316 73436 ?        Ssl  16:28   0:00 /usr/local/bin/python3.13 -Xfrozen_modules=off -m ipykernel_launcher -f /root/.local/share/jupyter/runtime/kernel-6bd8c74e-fd89-448c-9e6a-22de9783e8b5.json
root         490  1.7  3.9 1103836 79392 ?       Ssl  16:28   0:00 node /usr/bin/ijskernel --hide-undefined /root/.local/share/jupyter/runtime/kernel-1fe44cf5-e7f2-4ee3-82b8-24ac60d6d93f.json --protocol=5.1
root         504  0.1  1.9 728296 39900 ?        Sl   16:28   0:00 /usr/bin/node --eval (async function() { /*  * BSD 3-Clause License  *  * Copyright (c) 2018, Nicolas Riesco and others as credited in the AUTHORS file  * All rights reserved.  *  * Redistribution and use in source and binary forms, with or without  * modification, are permitted provided that the following conditions are met:  *  * 1. Redistributions of source code must retain the above copyright notice,  * this list of conditions and the following disclaimer.  *  * 2. Redistributions in binary form must reproduce the above copyright notice,  * this list of conditions and the following disclaimer in the documentation  * and/or other materials provided with the distribution.  *  * 3. Neither the name of the copyright holder nor the names of its contributors  * may be used to endorse or promote products derived from this software without  * specific prior written permission.  *  * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"  * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE  * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE  * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE  * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR  * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF  * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS  * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN  * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)  * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE  * POSSIBILITY OF SUCH DAMAGE.  *  */  /* eslint-disable no-unused-vars */ var console = require("console"); var stream = require("stream"); var util = require("util"); var vm = require("vm"); /* eslint-enable no-unused-vars */  /*  * BSD 3-Clause License  *  * Copyright (c) 2015, Nicolas Riesco and others as credited in the AUTHORS file  * All rights reserved.  *  * Redistribution and use in source and binary forms, with or without  * modification, are permitted provided that the following conditions are met:  *  * 1. Redistributions of source code must retain the above copyright notice,  * this list of conditions and the following disclaimer.  *  * 2. Redistributions in binary form must reproduce the above copyright notice,  * this list of conditions and the following disclaimer in the documentation  * and/or other materials provided with the distribution.  *  * 3. Neither the name of the copyright holder nor the names of its contributors  * may be used to endorse or promote products derived from this software without  * specific prior written permission.  *  * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"  * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE  * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE  * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE  * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR  * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF  * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS  * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN  * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)  * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE  * POSSIBILITY OF SUCH DAMAGE.  *  */  /* global console */ /* global stream */ /* global util */  /* global Promise */  /* global log */ /* global Display */  function Stdout(contextId, opt) {     stream.Transform.call(this, opt);      this._contextId = contextId; }  Stdout.prototype = Object.create(stream.Transform.prototype);  Stdout.prototype._transform = function(data, encoding, callback) {     var response = {         id: this._contextId,         stdout: data.toString(),     };     log("STDOUT:", response);     process.send(response);     this.push(data);     callback(); };  function Stderr(contextId, opt) {     stream.Transform.call(this, opt);      this._contextId = contextId; }  Stderr.prototype = Object.create(stream.Transform.prototype);  Stderr.prototype._transform = function(data, encoding, callback) {     var response = {         id: this._contextId,         stderr: data.toString(),     };     log("STDERR:", response);     process.send(response);     this.push(data);     callback(); };  function Requester(contextId) {     // context id     this.contextId = contextId;      // id for next request     this.requestId = 0;      // callback associated with a request (indexed by id)     this.callbacks = {};      // the Promise resolve callback associated with a request (indexed by id)     this.resolves = {};      // the Promise reject callback associated with a request (indexed by id)     this.rejects = {}; }  // send a request Requester.prototype.send = function send(request, callback) {     var requestId = this.requestId++;     request.id = requestId;      if (callback) {         this.callbacks[requestId] = callback;     }      var promise;     if (global.Promise) {         promise = new Promise(function(resolve, reject) {             this.resolves[requestId] = resolve;             this.rejects[requestId] = reject;         }.bind(this));     }      process.send({         id: this.contextId,         request: request,     });      return promise; };  // pass reply to the callbacks associated with a request Requester.prototype.receive = function receive(requestId, reply) {     var callback = this.callbacks[requestId];     if (callback) {         delete this.callbacks[requestId];         callback(null, reply);     }      var resolve = this.resolves[requestId];     if (resolve) {         delete this.resolves[requestId];         delete this.rejects[requestId];         resolve(reply);     } };  function Context(id) {     this.id = id;      this.requester = new Requester(this.id);      this.stdout = new Stdout(this.id);     this.stderr = new Stderr(this.id);     this.console = new console.Console(this.stdout, this.stderr);      this._capturedStdout = null;     this._capturedStderr = null;     this._capturedConsole = null;      this._async = false;     this._done = false;      // `$$` provides an interface for users to access the execution context     this.$$ = Object.create(null);      // `$$.config` provides an interface to configure NEL's features.     // * If `$$.config.awaitExecution` is set to `true`,     //   then execution requests that return a Promise will automatically     //   invoke `$$.async()` and the execution result will be replaced with the     //   value resolved by the promise.     Context.config = Context.config || {         awaitExecution: false,     };     Object.defineProperty(this.$$, "config", {         value: Context.config,         configurable: false,         writable: false,         enumerable: false,     });      this.$$.async = (function async(value) {         this._async = (arguments.length === 0) ? true : !!value;         return this._async;     }).bind(this);      this.$$.done = (function done(result) {         this.send({             mime: toMime(result),         }, false);     }).bind(this);      this.$$.sendResult = resolvePromise.call(this, this.sendResult);      this.$$.sendError = resolvePromise.call(this, this.sendError);      this.$$.mime = resolvePromise.call(this,         function sendMime(mimeBundle, keepAlive) {             this.send({                 mime: mimeBundle,             }, keepAlive);         }     );      this.$$.text = resolvePromise.call(this,         function sendText(text, keepAlive) {             this.send({                 mime: {                     "text/plain": text,                 },             }, keepAlive);         }     );      this.$$.html = resolvePromise.call(this,         function sendHtml(html, keepAlive) {             this.send({                 mime: {                     "text/html": html,                 },             }, keepAlive);         }     );      this.$$.svg = resolvePromise.call(this,         function sendSvg(svg, keepAlive) {             this.send({                 mime: {                     "image/svg+xml": svg,                 },             }, keepAlive);         }     );      this.$$.png = resolvePromise.call(this,         function sendPng(png, keepAlive) {             this.send({                 mime: {                     "image/png": png,                 },             }, keepAlive);         }     );      this.$$.jpeg = resolvePromise.call(this,         function sendJpeg(jpeg, keepAlive) {             this.send({                 mime: {                     "image/jpeg": jpeg,                 },             }, keepAlive);         }     );      this.$$.json = resolvePromise.call(this,         function sendJson(json, keepAlive) {             this.send({                 mime: {                     "application/json": json,                 },             }, keepAlive);         }     );      this.$$.input = (function input(options, callback) {         this.$$.async();          var inputRequest = {             input: options,         };          var inputCallback;         if (typeof callback === "function") {             inputCallback = function inputCallback(error, reply) {                 callback(error, reply.input);             };         }          var promise = this.requester.send(inputRequest, inputCallback);         if (promise) {             return promise.then(function(reply) { return reply.input; });         }     }).bind(this);      this.$$.display = (function createDisplay(id) {         return (arguments.length === 0) ?             new Display(this.id) :             new Display(this.id, id);     }).bind(this);      this.$$.clear = (function clear(options) {         process.send({             id: this.id,             request: {                 clear: options || {},             },         });     }).bind(this);      function isPromise(output) {         if (!global.Promise || typeof global.Promise !== "function") {             return false;         }         return output instanceof global.Promise;     }      function resolvePromise(outputHandler) {         return function(output, keepAlive) {             if (isPromise(output)) {                 this.$$.async();                  output.then(function(resolvedOutput) {                     outputHandler.call(this, resolvedOutput, keepAlive);                 }.bind(this)).catch(function(error) {                     this.sendError(error, false);                 }.bind(this));                  return;             }              outputHandler.apply(this, arguments);         }.bind(this);     } }  Context.prototype.sendResult = function sendResult(result, keepAlive) {     this.send({         mime: toMime(result),     }, keepAlive); };  Context.prototype.sendError = function sendError(error, keepAlive) {     this.send({         error: formatError(error),     }, keepAlive); };  Context.prototype.send = function send(message, keepAlive) {     message.id = this.id;     message.end = !keepAlive;      if (this._done) {         log("SEND: Warning! Message dropped:", message);         return;     }      if (keepAlive) {         this.$$.async();     } else {         this.done();     }      log("SEND:", message);      process.send(message); };  Context.prototype.done = function done() {     this._async = false;      if (this._done) {         log("DONE: Warning! Context#done already invoked");     }     this._done = true;      releaseContext(this.id, function onMissing() {         log("DONE: Warning! Context already released");     }); };  Context.prototype.captureGlobalContext = function captureGlobalContext() {     this._capturedStdout = process.stdout;     this._capturedStderr = process.stderr;     this._capturedConsole = console;      this.stdout.pipe(this._capturedStdout);     this.stderr.pipe(this._capturedStderr);     this.console.Console = this._capturedConsole.Console;      delete process.stdout;     process.stdout = this.stdout;      delete process.stderr;     process.stderr = this.stderr;      delete global.console;     global.console = this.console;      delete global.$$;     global.$$ = this.$$;      if (typeof global.$$mimer$$ !== "function") {         global.$$mimer$$ = defaultMimer;     }      delete global.$$mime$$;     Object.defineProperty(global, "$$mime$$", {         set: this.$$.mime,         configurable: true,         enumerable: false,     });      delete global.$$html$$;     Object.defineProperty(global, "$$html$$", {         set: this.$$.html,         configurable: true,         enumerable: false,     });      delete global.$$svg$$;     Object.defineProperty(global, "$$svg$$", {         set: this.$$.svg,         configurable: true,         enumerable: false,     });      delete global.$$png$$;     Object.defineProperty(global, "$$png$$", {         set: this.$$.png,         configurable: true,         enumerable: false,     });      delete global.$$jpeg$$;     Object.defineProperty(global, "$$jpeg$$", {         set: this.$$.jpeg,         configurable: true,         enumerable: false,     });      delete global.$$async$$;     Object.defineProperty(global, "$$async$$", {         get: (function() {             return this._async;         }).bind(this),         set: (function(value) {             this._async = !!value;         }).bind(this),         configurable: true,         enumerable: false,     });      global.$$done$$ = this.$$.done.bind(this);      if (!global.hasOwnProperty("$$defaultMimer$$")) {         Object.defineProperty(global, "$$defaultMimer$$", {             value: defaultMimer,             configurable: false,             writable: false,             enumerable: false,         });     } };  Context.prototype.releaseGlobalContext = function releaseGlobalContext() {     if (process.stdout === this.stdout) {         this.stdout.unpipe();          delete process.stdout;         process.stdout = this._capturedStdout;          this._capturedStdout = null;     }      if (process.stderr === this.stderr) {         this.stderr.unpipe();          delete process.stderr;         process.stderr = this._capturedStderr;          this._capturedStderr = null;     }      if (global.console === this.console) {         delete global.console;         global.console = this._capturedConsole;          this._capturedConsole = null;     } };  function formatError(error) {     return {         ename: (error && error.name) ?             error.name : typeof error,         evalue: (error && error.message) ?             error.message : util.inspect(error),         traceback: (error && error.stack) ?             error.stack.split("\n") : [],     }; }  function toMime(result) {     var mimer = (typeof global.$$mimer$$ === "function") ?         global.$$mimer$$ :         defaultMimer;     return mimer(result); }  function defaultMimer(result) { // eslint-disable-line complexity     if (typeof result === "undefined") {         return {             "text/plain": "undefined"         };     }      if (result === null) {         return {             "text/plain": "null"         };     }      var mime;     if (result._toMime) {         try {             mime = result._toMime();         } catch (error) {}     }     if (typeof mime !== "object") {         mime = {};     }      if (!("text/plain" in mime)) {         try {             mime["text/plain"] = util.inspect(result);         } catch (error) {}     }      if (result._toHtml && !("text/html" in mime)) {         try {             mime["text/html"] = result._toHtml();         } catch (error) {}     }      if (result._toSvg && !("image/svg+xml" in mime)) {         try {             mime["image/svg+xml"] = result._toSvg();         } catch (error) {}     }      if (result._toPng && !("image/png" in mime)) {         try {             mime["image/png"] = result._toPng();         } catch (error) {}     }      if (result._toJpeg && !("image/jpeg" in mime)) {         try {             mime["image/jpeg"] = result._toJpeg();         } catch (error) {}     }      return mime; }  // Context factory function getContext(id, onMissing) {     var cache = getContext.cache = getContext.cache || {};     var context = cache[id];     if (!context) {         onMissing && onMissing();         context = cache[id] = new Context(id);     }     return context; }  function releaseContext(id, onMissing) {     var context = getContext.cache[id];     if (context) {         log("releaseContext: Releasing context", id);         delete getContext.cache[id];     } else {         log("releaseContext: Warning! Context already released", id);         onMissing && onMissing();     } }  // Capture global context (it releases last capture if any) function captureGlobalContext(context) { // eslint-disable-line no-unused-vars     var last = captureGlobalContext.last;     last && last.releaseGlobalContext();     context.captureGlobalContext();     captureGlobalContext.last = context; } /*  * BSD 3-Clause License  *  * Copyright (c) 2017, Nicolas Riesco and others as credited in the AUTHORS file  * All rights reserved.  *  * Redistribution and use in source and binary forms, with or without  * modification, are permitted provided that the following conditions are met:  *  * 1. Redistributions of source code must retain the above copyright notice,  * this list of conditions and the following disclaimer.  *  * 2. Redistributions in binary form must reproduce the above copyright notice,  * this list of conditions and the following disclaimer in the documentation  * and/or other materials provided with the distribution.  *  * 3. Neither the name of the copyright holder nor the names of its contributors  * may be used to endorse or promote products derived from this software without  * specific prior written permission.  *  * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"  * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE  * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE  * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE  * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR  * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF  * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS  * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN  * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)  * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE  * POSSIBILITY OF SUCH DAMAGE.  *  */  function Display(context_id, display_id) { // eslint-disable-line no-unused-vars     var send;      this.mime = function mime(mimeBundle) {         send(mimeBundle);     };      this.text = function text(text) {         send({"text/plain": text});     };      this.html = function html(html) {         send({"text/html": html});     };      this.svg = function svg(svg) {         send({"image/svg+xml": svg});     };      this.png = function png(png) {         send({"image/png": png});     };      this.jpeg = function jpeg(jpeg) {         send({"image/jpeg": jpeg});     };      this.json = function json(json) {         send({"application/json": json});     };      this.close = function close() {         process.send({             id: context_id,             display: {                 close: display_id,             },         });     };      if (arguments.length < 2) {         // case: without a display_id         send = function send(mime) {             process.send({                 id: context_id,                 display: {                     mime: mime,                 },             });         };     } else {         // case: with a display_id         send = function send(mime) {             process.send({                 id: context_id,                 display: {                     display_id: display_id,                     mime: mime,                 },             });         };          // open the display_id         process.send({             id: context_id,             display: {                 open: display_id,             },         });     } }  /*  * BSD 3-Clause License  *  * Copyright (c) 2015, Nicolas Riesco and others as credited in the AUTHORS file  * All rights reserved.  *  * Redistribution and use in source and binary forms, with or without  * modification, are permitted provided that the following conditions are met:  *  * 1. Redistributions of source code must retain the above copyright notice,  * this list of conditions and the following disclaimer.  *  * 2. Redistributions in binary form must reproduce the above copyright notice,  * this list of conditions and the following disclaimer in the documentation  * and/or other materials provided with the distribution.  *  * 3. Neither the name of the copyright holder nor the names of its contributors  * may be used to endorse or promote products derived from this software without  * specific prior written permission.  *  * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"  * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE  * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE  * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE  * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR  * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF  * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS  * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN  * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)  * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE  * POSSIBILITY OF SUCH DAMAGE.  *  */  /* global util */ /* global vm */  /* global defaultMimer */  /* global getContext */ /* global captureGlobalContext */  // Setup logger var DEBUG = !!process.env.DEBUG; var log = DEBUG ?     function log() {         process.send({             log: "SERVER: " + util.format.apply(this, arguments),         });     } :     function noop() {};  // Set global.$$defaultMimer$$ Object.defineProperty(global, "$$defaultMimer$$", {     value: defaultMimer,     configurable: false,     writable: false,     enumerable: false, });  // Init IPC server init();  return;  function init() {     process.on("message", onMessage.bind(this));      process.on("uncaughtException", onUncaughtException.bind(this));      process.send({         status: "online",     }); }  function onUncaughtException(error) {     log("UNCAUGHTEXCEPTION:", error.stack);     process.send({         stderr: error.stack.toString(),     }); }  async function onMessage(message) {     log("RECEIVED:", message);      var action = message[0];     var code = message[1];     var id = message[2];      try {         var context = getContext(id, function onMissing() {             if (action === "reply") {                 throw new Error("NEL: Received a reply for a missing context");             }         });          captureGlobalContext(context);          if (action === "getAllPropertyNames") {             await onNameRequest(code, context);         } else if (action === "inspect") {             await onInspectRequest(code, context);         } else if (action === "run") {             await onRunRequest(code, context);         } else if (action === "reply") {             onReply(message, context);         } else {             throw new Error("NEL: Unhandled action: " + action);         }     } catch (error) {         context.$$.sendError(error);     } }  function onReply(message, context) {     var reply = message[1];     var requestId = message[3];     context.requester.receive(requestId, reply); }  async function onNameRequest(code, context) {     var message = {         id: context.id,         names: getAllPropertyNames(await run(code)),         end: true,     };     context.send(message); }  async function onInspectRequest(code, context) {     var message = {         id: context.id,         inspection: inspect(await run(code)),         end: true,     };     context.send(message); }  async function onRunRequest(code, context) {     var result = await run(code);      // If a result has already been sent, do not send this result.     if (context._done) {         return;     }      // If async mode has been enabled, do not send this result.     if (context._async) {         return;     }      // If no result has been sent yet and async mode has not been enabled,     // send this result.     if (context.$$.config.awaitExecution) {         context.$$.sendResult(result);     } else {         context.sendResult(result);     }      return; }  function getAllPropertyNames(object) {     var propertyList = [];      if (object === undefined) {         return [];     }      if (object === null) {         return [];     }      var prototype;     if (typeof object === "boolean") {         prototype = Boolean.prototype;     } else if (typeof object === "number") {         prototype = Number.prototype;     } else if (typeof object === "string") {         prototype = String.prototype;     } else {         prototype = object;     }      var prototypeList = [prototype];      function pushToPropertyList(e) {         if (propertyList.indexOf(e) === -1) {             propertyList.push(e);         }     }      while (prototype) {         var names = Object.getOwnPropertyNames(prototype).sort();         names.forEach(pushToPropertyList);          prototype = Object.getPrototypeOf(prototype);         if (prototype === null) {             break;         }          if (prototypeList.indexOf(prototype) === -1) {             prototypeList.push(prototype);         }     }      return propertyList; }  function inspect(object) {     if (object === undefined) {         return {             string: "undefined",             type: "Undefined",         };     }      if (object === null) {         return {             string: "null",             type: "Null",         };     }      if (typeof object === "boolean") {         return {             string: object ? "true" : "false",             type: "Boolean",             constructorList: ["Boolean", "Object"],         };     }      if (typeof object === "number") {         return {             string: util.inspect(object),             type: "Number",             constructorList: ["Number", "Object"],         };     }      if (typeof object === "string") {         return {             string: object,             type: "String",             constructorList: ["String", "Object"],             length: object.length,         };     }      if (typeof object === "function") {         return {             string: object.toString(),             type: "Function",             constructorList: ["Function", "Object"],             length: object.length,         };     }      var constructorList = getConstructorList(object);     var result = {         string: toString(object),         type: constructorList[0] || "",         constructorList: constructorList,     };      if ("length" in object) {         result.length = object.length;     }      return result;      function toString(object) {         try {             return util.inspect(object.valueOf());         } catch (e) {             return util.inspect(object);         }     }      function getConstructorList(object) {         var constructorList = [];          for (             var prototype = Object.getPrototypeOf(object);             prototype && prototype.constructor;             prototype = Object.getPrototypeOf(prototype)         ) {             constructorList.push(prototype.constructor.name);         }          return constructorList;     } }  async function run(code) {     return await vm.runInThisContext(code, { importModuleDynamically: vm.constants.USE_MAIN_CONTEXT_DEFAULT_LOADER }); }  })();
root         512  0.0  0.1  11716  3020 ?        S<   16:28   0:00 socat -d -d -d TCP4-LISTEN:35769,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:35769
root         513  0.0  0.1  11716  3024 ?        S<   16:28   0:00 socat -d -d -d TCP4-LISTEN:47945,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:47945
root         514  0.0  0.1  11716  3024 ?        S<   16:28   0:00 socat -d -d -d TCP4-LISTEN:34675,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:34675
root         515  0.0  0.1  11716  3028 ?        S<   16:28   0:00 socat -d -d -d TCP4-LISTEN:44461,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:44461
root         516  0.0  0.1  11716  3024 ?        S<   16:28   0:00 socat -d -d -d TCP4-LISTEN:39379,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:39379
root         517  0.0  0.1  11716  3020 ?        S<   16:28   0:00 socat -d -d -d TCP4-LISTEN:41435,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:41435
root         518  0.0  0.1  11716  3024 ?        S<   16:28   0:00 socat -d -d -d TCP4-LISTEN:43501,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:43501
root         521  0.0  0.1  11716  3024 ?        S<   16:28   0:00 socat -d -d -d TCP4-LISTEN:35105,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:35105
root         523  0.0  0.1  11716  3024 ?        S<   16:28   0:00 socat -d -d -d TCP4-LISTEN:60465,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:60465
root         524  0.0  0.1  11716  3028 ?        S<   16:28   0:00 socat -d -d -d TCP4-LISTEN:60493,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:60493
root         525  0.0  0.1  11716  3024 ?        S<   16:28   0:00 socat -d -d -d TCP4-LISTEN:53335,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:53335
root        1315  0.0  0.0      0     0 ?        I    16:28   0:00 [kworker/u4:5-ext4-rsv-conversion]
user        1429  0.0  0.1   4056  3344 ?        S    16:28   0:00 /bin/bash -l -c rm -f /home/user/run_recon.sh /home/user/local_recon_raw.txt /home/user/local_recon_report.md cat > /tmp/run_recon.sh <<'EOF' #!/usr/bin/env bash set +e OUT=/tmp/local_recon_raw.txt : > "$OUT" { echo '===== A. ??????????????? =====' echo '$ whoami; id; uname -a; cat /etc/os-release 2>/dev/null | head -3; cat /proc/1/cgroup 2>/dev/null' whoami; id; uname -a; cat /etc/os-release 2>/dev/null | head -3; cat /proc/1/cgroup 2>/dev/null  echo; echo '===== B. ???????????????????????? ====='; echo '$ env | sort' env | sort  echo; echo '===== C. ?????? ====='; echo '$ cat /etc/hosts; cat /etc/resolv.conf; ip addr 2>/dev/null || ifconfig 2>/dev/null; ip route 2>/dev/null; ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null' cat /etc/hosts; cat /etc/resolv.conf if command -v ip >/dev/null 2>&1; then ip addr 2>/dev/null; else echo 'ip: ?????????'; if command -v ifconfig >/dev/null 2>&1; then ifconfig 2>/dev/null; else echo 'ifconfig: ?????????'; fi; fi if command -v ip >/dev/null 2>&1; then ip route 2>/dev/null; else echo 'ip route: ?????????'; fi if command -v ss >/dev/null 2>&1; then ss -tlnp 2>/dev/null; else echo 'ss: ?????????'; if command -v netstat >/dev/null 2>&1; then netstat -tlnp 2>/dev/null; else echo 'netstat: ?????????'; fi; fi  echo; echo '===== D. ?????? ====='; echo '$ ps aux 2>/dev/null' if command -v ps >/dev/null 2>&1; then ps aux 2>/dev/null; else echo 'ps: ?????????'; fi  echo; echo '===== E. ???????????? ====='; echo '$ ls -la /; ls -la /home/user 2>/dev/null; ls -la ~ 2>/dev/null' if command -v ls >/dev/null 2>&1; then ls -la /; ls -la /home/user 2>/dev/null; ls -la ~ 2>/dev/null; else echo 'ls: ?????????'; fi  echo; echo '===== F. ???????????????????????? ====='; echo '$ for p in 80 443 3000 5000 8000 8080 8081 8888 9000; do curl -s -m 2 -o /dev/null -w "127.0.0.1:$p -> %{http_code}\\n" http://127.0.0.1:$p; done' if command -v curl >/dev/null 2>&1; then for p in 80 443 3000 5000 8000 8080 8081 8888 9000; do curl -s -m 2 -o /dev/null -w "127.0.0.1:$p -> %{http_code}\n" http://127.0.0.1:$p; done; else echo 'curl: ?????????'; fi  echo; echo '===== G. ??????????????????????????????????????? ====='; echo '$ grep -rIl -E "MODEL|model_id|api_key|base_url|proxy|gateway|provider" /etc /opt /usr/local/etc /home/user 2>/dev/null | head -40' if command -v grep >/dev/null 2>&1; then grep -rIl -E 'MODEL|model_id|api_key|base_url|proxy|gateway|provider' /etc /opt /usr/local/etc /home/user 2>/dev/null | head -40; else echo 'grep: ?????????'; fi } >> "$OUT" cp "$OUT" /home/user/local_recon_raw.txt EOF chmod +x /tmp/run_recon.sh /tmp/run_recon.sh wc -lc /home/user/local_recon_raw.txt sha256sum /home/user/local_recon_raw.txt
user        1435  0.0  0.1   4056  3092 ?        S    16:28   0:00 bash /tmp/run_recon.sh
user        1449  0.0  0.1   6392  3712 ?        R    16:28   0:00 ps aux

===== E. 文件系统 =====
$ ls -la /; ls -la /home/user 2>/dev/null; ls -la ~ 2>/dev/null
total 37
drwxr-xr-x  19 root root  4096 Jul 23 18:05 .
drwxr-xr-x  19 root root  4096 Jul 23 18:05 ..
-rw-r--r--   1 root root   107 Jul 23 18:05 .e2b
lrwxrwxrwx   1 root root     7 Jul  4 09:05 bin -> usr/bin
drwxr-xr-x   2 root root    60 Jul  4 09:05 boot
drwxrwxrwx   2 root root    60 Jul 23 18:05 code
drwxr-xr-x   8 root root  2620 Jul 23 18:05 dev
drwxr-xr-x  69 root root  4096 Jul 23 18:05 etc
drwxr-xr-x   3 root root    60 Jul 23 15:09 home
lrwxrwxrwx   1 root root     7 Jul  4 09:05 lib -> usr/lib
lrwxrwxrwx   1 root root     9 Jul  4 09:05 lib64 -> usr/lib64
drwx------   2 root root 12288 Jul 23 15:09 lost+found
drwxr-xr-x   2 root root    60 Jul 13 00:00 media
drwxr-xr-x   2 root root    60 Jul 13 00:00 mnt
drwxr-xr-x   2 root root    60 Jul 13 00:00 opt
dr-xr-xr-x 150 root root     0 Jul 23 18:05 proc
drwx------  11 root root  4096 Jul 23 18:05 root
drwxr-xr-x  17 root root   520 Jul 23 18:05 run
lrwxrwxrwx   1 root root     8 Jul  4 09:05 sbin -> usr/sbin
drwxr-xr-x   2 root root    60 Jul 13 00:00 srv
dr-xr-xr-x  12 root root     0 Oct  5 16:28 sys
drwxrwxrwt   8 root root   200 Oct  5 16:28 tmp
drwxr-xr-x  12 root root  4096 Jul 23 15:09 usr
drwxr-xr-x  11 root root  4096 Jul 23 15:09 var
total 0
drwx------ 2 user user 128 Oct  5 16:28 .
drwxr-xr-x 3 root root  60 Jul 23 15:09 ..
total 0
drwx------ 2 user user 128 Oct  5 16:28 .
drwxr-xr-x 3 root root  60 Jul 23 15:09 ..

===== F. 本机服务快速探测 =====
$ for p in 80 443 3000 5000 8000 8080 8081 8888 9000; do curl -s -m 2 -o /dev/null -w "127.0.0.1:$p -> %{http_code}\\n" http://127.0.0.1:$p; done
127.0.0.1:80 -> 000
127.0.0.1:443 -> 000
127.0.0.1:3000 -> 000
127.0.0.1:5000 -> 000
127.0.0.1:8000 -> 000
127.0.0.1:8080 -> 000
127.0.0.1:8081 -> 000
127.0.0.1:8888 -> 200
127.0.0.1:9000 -> 000

===== G. 配置文件浅层搜索（关键词） =====
$ grep -rIl -E "MODEL|model_id|api_key|base_url|proxy|gateway|provider" /etc /opt /usr/local/etc /home/user 2>/dev/null | head -40
/etc/ssh/ssh_config
/etc/ssl/openssl.cnf
/etc/subversion/servers
/etc/systemd/system/envd.service
/etc/group
/etc/group-
/etc/mime.types
/etc/passwd
/etc/passwd-
/etc/protocols
/etc/services
/etc/wgetrc
/etc/nfs.conf
```

## 推断与置信度 / Inference and confidence
- 运行环境为 E2B 提供的 Debian 13 本地沙箱。置信度：高。
- `127.0.0.1:8888` 在快速 HTTP 探测时返回 200。置信度：高。
