# MohawkRemotePython

**To start Mohawk Server. Command line:**
```
cd C:\Program Files\Ziath\Mohawk\
```
```
MohawkServer.exe
```
**To start Mohawk Server Simulation. Command Line:**
```
cd C:\Program Files\Ziath\Mohawk\
```
```
MohawkServer.exe -ss
```
**To start Mohawk Example with python 3. Command Line**
```
MohawkRemoteExample.py
```


**Recommended log4j2.xml DEV DEBUG configuration**


Modify log configuration file: C:\Program Files\Ziath\Mohawk\log4j2.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration>
    <Appenders>
        <RollingFile name="RollingFile" fileName="${sys:log.dir}/logs/mohawk.log" filePattern="${sys:log.dir}/logs/mohawk-%i.log">
            <PatternLayout>
                <pattern>[%-5level] %d{yyyy-MM-dd HH:mm:ss.SSS} [%t] %c{1} - %msg%n</pattern>
            </PatternLayout>
            <Policies>
				<SizeBasedTriggeringPolicy size="20 MB" />
            </Policies>
        </RollingFile>
 
        <Console name="Console" target="SYSTEM_OUT">
            <PatternLayout   pattern="[%-5level] %d{yyyy-MM-dd HH:mm:ss.SSS} [%t] %c{1} - %msg%n" />
        </Console>
    </Appenders>
    
    <Loggers>
		<Logger name="com.ziath.datapaq.barcodelinearreader" level="error" additivity="false">
			<AppenderRef ref="Console" />
			<AppenderRef ref="RollingFile" />
		</Logger>
		
		<Logger name="com.ziath.driver" level="error" additivity="false">
			<AppenderRef ref="Console" />
			<AppenderRef ref="RollingFile" />
		</Logger>
		
		<Logger name="com.ziath.comms" level="error" additivity="false">
			<AppenderRef ref="Console" />
			<AppenderRef ref="RollingFile" />
		</Logger>
		
		<Root level="debug">
			<AppenderRef ref="Console" />
			<AppenderRef ref="RollingFile" />
		</Root>
    </Loggers>
</Configuration>
```
