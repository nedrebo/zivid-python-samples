"""
Capture point clouds, with color, from the Zivid camera.

"""

import datetime

import zivid


def _main() -> None:
    app = zivid.Application()

    print("Connecting to camera")
    camera = app.connect_camera()

    print("Configuring settings")
    settings = zivid.Settings()
    settings.experimental.engine = "phase"
    settings.acquisitions.append(zivid.Settings.Acquisition())
    settings.acquisitions[0].aperture = 5.66
    settings.acquisitions[0].exposure_time = datetime.timedelta(microseconds=6500)
    settings.processing.filters.outlier.removal.enabled = True
    settings.processing.filters.outlier.removal.threshold = 5.0

    print("Capturing frame")
    with camera.capture(settings) as frame:
        data_file = "Frame.zdf"
        print(f"Saving frame to file: {data_file}")
        frame.save(data_file)

        data_file_ply = "PointCloud.ply"
        print(f"Exporting point cloud to file: {data_file_ply}")
        frame.save(data_file_ply)


if __name__ == "__main__":
    _main()
