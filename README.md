<p>Example usage</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ python api.py
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader
</pre></div>
</div>
<p>GET the list</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ curl http://localhost:5000/todos
{&quot;todo1&quot;: {&quot;task&quot;: &quot;build an API&quot;}, &quot;todo3&quot;: {&quot;task&quot;: &quot;profit!&quot;}, &quot;todo2&quot;: {&quot;task&quot;: &quot;?????&quot;}}
</pre></div>
</div>
<p>GET a single task</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ curl http://localhost:5000/todos/todo3
{&quot;task&quot;: &quot;profit!&quot;}
</pre></div>
</div>
<p>DELETE a task</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ curl http://localhost:5000/todos/todo2 -X DELETE -v

&gt; DELETE /todos/todo2 HTTP/1.1
&gt; User-Agent: curl/7.19.7 (universal-apple-darwin10.0) libcurl/7.19.7 OpenSSL/0.9.8l zlib/1.2.3
&gt; Host: localhost:5000
&gt; Accept: */*
&gt;
* HTTP 1.0, assume close after body
&lt; HTTP/1.0 204 NO CONTENT
&lt; Content-Type: application/json
&lt; Content-Length: 0
&lt; Server: Werkzeug/0.8.3 Python/2.7.2
&lt; Date: Mon, 01 Oct 2012 22:10:32 GMT
</pre></div>
</div>
<p>Add a new task</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ curl http://localhost:5000/todos -d &quot;task=something new&quot; -X POST -v

&gt; POST /todos HTTP/1.1
&gt; User-Agent: curl/7.19.7 (universal-apple-darwin10.0) libcurl/7.19.7 OpenSSL/0.9.8l zlib/1.2.3
&gt; Host: localhost:5000
&gt; Accept: */*
&gt; Content-Length: 18
&gt; Content-Type: application/x-www-form-urlencoded
&gt;
* HTTP 1.0, assume close after body
&lt; HTTP/1.0 201 CREATED
&lt; Content-Type: application/json
&lt; Content-Length: 25
&lt; Server: Werkzeug/0.8.3 Python/2.7.2
&lt; Date: Mon, 01 Oct 2012 22:12:58 GMT
&lt;
* Closing connection #0
{&quot;task&quot;: &quot;something new&quot;}
</pre></div>
</div>
<p>Update a task</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ curl http://localhost:5000/todos/todo3 -d &quot;task=something different&quot; -X PUT -v

&gt; PUT /todos/todo3 HTTP/1.1
&gt; Host: localhost:5000
&gt; Accept: */*
&gt; Content-Length: 20
&gt; Content-Type: application/x-www-form-urlencoded
&gt;
* HTTP 1.0, assume close after body
&lt; HTTP/1.0 201 CREATED
&lt; Content-Type: application/json
&lt; Content-Length: 27
&lt; Server: Werkzeug/0.8.3 Python/2.7.3
&lt; Date: Mon, 01 Oct 2012 22:13:00 GMT
&lt;
* Closing connection #0
{&quot;task&quot;: &quot;something different&quot;}
</pre></div>
</div>
</div>
</div>


          </div>
        </div>
      </div>
      <div class="sphinxsidebar" role="navigation" aria-label="main navigation">
        <div class="sphinxsidebarwrapper"><p class="logo"><a href="index.html">
  <img class="logo" src="_static/flask-restful-small.png" alt="Logo"
    style="margin-left: -10px"/>
</a></p>
