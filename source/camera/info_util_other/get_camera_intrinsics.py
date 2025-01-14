"""
Read intrinsic parameters from the Zivid camera (OpenCV model) or estimate them from the point cloud.

Note: This example uses experimental SDK features, which may be modified, moved, or deleted in the future without notice.

"""

import zivid
from zivid.experimental import calibration


def _print_parameter_delta(label: str, fixed_value: float, estimated_value: float) -> None:
    delta = fixed_value - estimated_value
    if delta != 0:
        print(f"{label:>6}: {delta:6.2f} ({abs(100 * delta / fixed_value):6.2f}% )")


def _print_intrinsic_parameters_delta(
    fixed_intrinsics: zivid.CameraIntrinsics, estimated_intrinsics: zivid.CameraIntrinsics
) -> None:
    _print_parameter_delta("CX", fixed_intrinsics.camera_matrix.cx, estimated_intrinsics.camera_matrix.cx)
    _print_parameter_delta("CY", fixed_intrinsics.camera_matrix.cy, estimated_intrinsics.camera_matrix.cy)
    _print_parameter_delta("FX", fixed_intrinsics.camera_matrix.fx, estimated_intrinsics.camera_matrix.fx)
    _print_parameter_delta("FY", fixed_intrinsics.camera_matrix.fy, estimated_intrinsics.camera_matrix.fy)

    _print_parameter_delta("K1", fixed_intrinsics.distortion.k1, estimated_intrinsics.distortion.k1)
    _print_parameter_delta("K2", fixed_intrinsics.distortion.k2, estimated_intrinsics.distortion.k2)
    _print_parameter_delta("K3", fixed_intrinsics.distortion.k3, estimated_intrinsics.distortion.k3)
    _print_parameter_delta("P1", fixed_intrinsics.distortion.p1, estimated_intrinsics.distortion.p1)
    _print_parameter_delta("P2", fixed_intrinsics.distortion.p2, estimated_intrinsics.distortion.p2)


def _main():
    app = zivid.Application()

    print("Connecting to camera")
    camera = app.connect_camera()

    print("Getting camera intrinsics")
    intrinsics = calibration.intrinsics(camera)
    print(intrinsics)

    output_file = "Intrinsics.yml"
    print(f"Saving camera intrinsics to file: {output_file}")
    intrinsics.save(output_file)

    print("\nDifference between fixed intrinsics and estimated intrinsics for different apertures and temperatures:")

    for fnum in (11.31, 5.66, 2.83):
        settings = zivid.Settings(acquisitions=[zivid.Settings.Acquisition(aperture=fnum)])
        with camera.capture(settings=settings) as frame:
            estimated_intrinsics = calibration.estimate_intrinsics(frame)
            temperature = frame.state.temperature.lens
            print(f"\nAperture: {fnum:.2f}, Lens Temperature: {temperature:.2f}°C")
            _print_intrinsic_parameters_delta(intrinsics, estimated_intrinsics)


if __name__ == "__main__":
    _main()
