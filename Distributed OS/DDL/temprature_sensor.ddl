<device
	type="generic"
	connection="analog">

	<metadata>
		<name>temperature_sensor</name>
		<default_pins number="1">
			<pin id="0">0</pin>
		</default_pins>
	</metadata>
	<measurements>
		<measurement name="temprature_centigrade">
			10*P[0] - 5000 
		</measurement>
	</measurements>

</device>


