// This file is part of MatrixPilot.
//
//    http://code.google.com/p/gentlenav/
//
// Copyright 2009-2011 MatrixPilot Team
// See the AUTHORS.TXT file for a list of authors of MatrixPilot.
//
// MatrixPilot is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// MatrixPilot is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with MatrixPilot.  If not, see <http://www.gnu.org/licenses/>.


#include "defines.h"
#include "../libDCM/gpsParseCommon.h"
#include "../libUDB/heartbeat.h"
#include "config.h"

#if (USE_TELELOG == 1)
#include "telemetry_log.h"
#endif

#if (USE_USB == 1)
#include "preflight.h"
#endif

#if (CONSOLE_UART != 0)
#include "console.h"
#endif

#ifdef USE_FREERTOS

#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

#include "../libUDB/barometer.h"

//xSemaphoreHandle xBinarySemaphore;
xSemaphoreHandle xSemaphoreGPS;
xSemaphoreHandle xSemaphoreIMU;

//void ScheduleIMU(void)
void TriggerIMU(void)
{
	xSemaphoreGiveFromISR(xSemaphoreIMU, NULL);
}

void TriggerGPS(void)
{
	xSemaphoreGiveFromISR(xSemaphoreGPS, NULL);
}

static void TaskIMU(void* pvParameters)
{
	static int i = 0;

	while (1)
	{
		xSemaphoreTake(xSemaphoreIMU, portMAX_DELAY);
		udb_led_toggle(LED_BLUE);
		pulse();

		if (i++ > 200)
		{
			i = 0;
//			DPRINT("imu\r\n");
			udb_led_toggle(LED_ORANGE);
		}
//		vTaskDelay(1500 / portTICK_RATE_MS);
	}
//	vTaskDelete(NULL);
}

static void TaskGPS(void* pvParameters)
{
	while (1)
	{
//		xSemaphoreTake(xSemaphoreGPS, portMAX_DELAY);
//		DPRINT("gps\r\n");
		vTaskDelay(1000 / portTICK_RATE_MS);
#if (BAROMETER_ALTITUDE == 1)
		rxBarometer(NULL);
#endif // BAROMETER_ALTITUDE
	}
}

void init_tasks(void)
{
//	xTaskCreate(TaskIMU, (signed portCHAR*)"IMU", configMINIMAL_STACK_SIZE, (void*)&(xParameters[0]), tskIDLE_PRIORITY, NULL);

//	vSemaphoreCreateBinary(xBinarySemaphore);
	vSemaphoreCreateBinary(xSemaphoreIMU);
	vSemaphoreCreateBinary(xSemaphoreGPS);
	xTaskCreate(TaskIMU, (signed portCHAR*)"IMU", configMINIMAL_STACK_SIZE, NULL, tskIDLE_PRIORITY+3, NULL);
	xTaskCreate(TaskGPS, (signed portCHAR*)"GPS", configMINIMAL_STACK_SIZE, NULL, tskIDLE_PRIORITY+2, NULL);
}

void vApplicationIdleHook(void)
{
//	DPRINT(".");
//	while (1)
	{
#if (USE_TELELOG == 1)
		telemetry_log();
#endif
#if (USE_USB == 1)
		USBPollingService();
#endif
#if (CONSOLE_UART != 0 && SILSIM == 0)
		console();
#endif
		udb_run();
	}
//	return 0;
}

#endif // USE_FREERTOS
