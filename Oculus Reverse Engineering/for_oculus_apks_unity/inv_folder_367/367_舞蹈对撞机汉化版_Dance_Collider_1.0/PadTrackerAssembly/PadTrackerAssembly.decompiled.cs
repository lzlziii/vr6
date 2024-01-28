using System;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;

[assembly: AssemblyTitle("PadTrackerAssembly")]
[assembly: AssemblyDescription("")]
[assembly: AssemblyConfiguration("")]
[assembly: AssemblyCompany("Microsoft")]
[assembly: AssemblyProduct("PadTrackerAssembly")]
[assembly: AssemblyCopyright("Copyright © Microsoft 2014")]
[assembly: AssemblyTrademark("")]
[assembly: ComVisible(false)]
[assembly: Guid("816ae558-fd8d-46f8-a901-8f55c9f9d60e")]
[assembly: AssemblyFileVersion("1.0.0.0")]
[assembly: CompilationRelaxations(8)]
[assembly: RuntimeCompatibility(WrapNonExceptionThrows = true)]
[assembly: AssemblyVersion("1.0.0.0")]
namespace UnityEngine.PS4.Engines;

public enum ScePadTrackerStatus
{
	SCE_PAD_TRACKER_TRACKING,
	SCE_PAD_TRACKER_NOT_TRACKING,
	SCE_PAD_TRACKER_ROOM_CONFLICT,
	SCE_PAD_TRACKER_CALIBRATING
}
public struct ScePadTrackerImageCoordinates
{
	public ScePadTrackerStatus status;

	public float x;

	public float y;
}
public struct ScePadTrackerDataOLD
{
	public ScePadTrackerStatus imageCoordinate0_status;

	public float imageCoordinate0_x;

	public float imageCoordinate0_y;

	public ScePadTrackerStatus imageCoordinate1_status;

	public float imageCoordinate1_x;

	public float imageCoordinate1_y;
}
[Serializable]
public struct ScePadTrackerData
{
	[MarshalAs(UnmanagedType.ByValArray, SizeConst = 8, ArraySubType = UnmanagedType.SysUInt)]
	public ScePadTrackerImageCoordinates[] imageCoordinates;
}
public class PadTracker
{
	[DllImport("PadTrackerPlugin")]
	private static extern int PrxPadTrackerInitialise();

	[DllImport("PadTrackerPlugin")]
	private static extern int PrxPadTrackerShutdown();

	[DllImport("PadTrackerPlugin")]
	private static extern int PrxPadTrackerCalibrate();

	[DllImport("PadTrackerPlugin")]
	private static extern int PrxPadTrackerUpdate(ulong cameraFrameHandle, int[] controllerHandles);

	[DllImport("PadTrackerPlugin")]
	private static extern int PrxPadTrackerQueueUpdate(ulong cameraFrameHandle, int[] controllerHandles);

	[DllImport("PadTrackerPlugin")]
	private static extern int PrxPadTrackerReadState(int handle, out ScePadTrackerData data);

	[DllImport("PadTrackerPlugin")]
	private static extern int PrxPadTrackerReadState(int handle, IntPtr ptr);

	public static int Init()
	{
		return PrxPadTrackerInitialise();
	}

	public static int Term()
	{
		return PrxPadTrackerShutdown();
	}

	public static int Calibrate()
	{
		return PrxPadTrackerCalibrate();
	}

	public static int QueueUpdate(ulong cameraFrameHandle, int[] controllerHandles)
	{
		return PrxPadTrackerQueueUpdate(cameraFrameHandle, controllerHandles);
	}

	public static int Update(ulong cameraFrameHandle, int[] controllerHandles)
	{
		return PrxPadTrackerUpdate(cameraFrameHandle, controllerHandles);
	}

	public static int ReadState(int controllerhandle, out ScePadTrackerData data)
	{
		IntPtr intPtr = Marshal.AllocHGlobal(24);
		data = default(ScePadTrackerData);
		data.imageCoordinates = new ScePadTrackerImageCoordinates[2];
		float[] array = new float[6];
		int result = PrxPadTrackerReadState(controllerhandle, intPtr);
		Marshal.Copy(intPtr, array, 0, 6);
		data.imageCoordinates[0].status = (ScePadTrackerStatus)Marshal.ReadInt32(intPtr, 0);
		data.imageCoordinates[0].x = array[1];
		data.imageCoordinates[0].y = array[2];
		data.imageCoordinates[1].status = (ScePadTrackerStatus)Marshal.ReadInt32(intPtr, 12);
		data.imageCoordinates[1].x = array[4];
		data.imageCoordinates[1].y = array[5];
		Marshal.FreeHGlobal(intPtr);
		return result;
	}
}
