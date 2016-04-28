---
layout: post
title:  "Jetty基础介绍"
date:   2016-04-26 09:23:32
categories: Jetty 
---

以下内容为调查语义网过程中一些知识的积累及问题的总结，以备后用！


##相关资源连接

[jetty官网](http://www.eclipse.org/jetty/)

[非常好的jetty入门技术博客](http://blog.csdn.net/column/details/jettyinaction.html)

[jetty官方技术文档](http://wiki.eclipse.org/Jetty)

***

##Sample代码段


```java
package org.jetty.demo;

import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.server.handler.ContextHandlerCollection;
import org.eclipse.jetty.servlet.ServletContextHandler;
import org.eclipse.jetty.servlet.ServletHolder;
import org.eclipse.jetty.webapp.WebAppContext;

//启动类，入口
public class JettyServe {
    public static void main(String[] args) throws Exception {
        Server server = new Server(8089);  
        
        ContextHandlerCollection handler = new ContextHandlerCollection();  
        
        ServletContextHandler context = new ServletContextHandler(ServletContextHandler.SESSIONS);  
        context.setContextPath("/");  
  
        // http://localhost:8080/hello  
        context.addServlet(new ServletHolder(new HelloServlet()), "/hello");  
        // http://localhost:8080/hello/kongxx  
        context.addServlet(new ServletHolder(new HelloServlet("Hello Kongxx!")), "/hello/kongxx");  
  
        // http://localhost:8080/goodbye  
        context.addServlet(new ServletHolder(new GoodbyeServlet()), "/goodbye");  
        // http://localhost:8080/goodbye/kongxx  
        context.addServlet(new ServletHolder(new GoodbyeServlet("Goodbye kongxx!")), "/goodbye/kongxx");  
          
        handler.addHandler(context);
        
        //add webapp
        WebAppContext webcontext = new WebAppContext();
        
        //读取webapp配置文件信息
        //webcontext.setDescriptor("/home/qy/Documents/jetty-8.0.0.v20110901/contexts//mywebApp.xml");  
        
        //设置所有资源文件路径
        webcontext.setResourceBase("/home/qy/mywebApp"); 
        
        //设置webapp访问路径
        webcontext.setContextPath("/kaka");  
        
        webcontext.setClassLoader(  
            Thread.currentThread().getContextClassLoader());  
        handler.addHandler(webcontext);
        
        server.setHandler(handler);  
        
        server.start();  
        server.join(); 
    }
}

```

