import pytest

from schedlib import source as src
import ephem
import datetime as dt
import numpy as np

def test_Location():
    # Test case 1: Verify at() method returns a new ephem.Observer object with correct attributes
    location = src.Location(lat=51.5074, lon=-0.1278, elev=0)
    date = dt.datetime(2023, 1, 1)
    observer = location.at(date)
    assert isinstance(observer, ephem.Observer)
    assert observer.date == ephem.date(date)

    # Test case 2: Verify at() method returns a new ephem.Observer object for a different date
    location = src.Location(lat=40.7128, lon=-74.0060, elev=0)
    date1 = dt.datetime(2023, 1, 1)
    observer1 = location.at(date1)
    date2 = dt.datetime(2023, 1, 2)
    observer2 = location.at(date2)
    assert isinstance(observer2, ephem.Observer)
    assert observer2.date == ephem.date(date2)
    assert observer1 is not observer2

def test_get_source():
    source = src.get_source('sun')
    assert isinstance(source, ephem.Body)

def test_source_get_az_alt():
    # Test case 1: Verify azimuth and altitude values for a single time
    source = 'sun'
    times = [dt.datetime(2023, 1, 1, tzinfo=dt.timezone.utc)]
    expected_az = [240.15972382]
    expected_alt = [-9.02030811]
    az, alt = src._source_get_az_alt(source, times)
    assert np.allclose(az, expected_az)
    assert np.allclose(alt, expected_alt)

    times = [dt.datetime(2023, 1, 1)]
    # fail on timezone-unaware datetime
    with pytest.raises(ValueError):
        az, alt = src._source_get_az_alt(source, times)

    # Test case 2: Verify azimuth and altitude values for multiple times
    source = 'jupiter'
    times = [
        dt.datetime(2023, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc),
        dt.datetime(2023, 1, 2, 0, 0, 0, tzinfo=dt.timezone.utc),
        dt.datetime(2023, 1, 3, 0, 0, 0, tzinfo=dt.timezone.utc)
    ]
    expected_az = [302.09675348, 301.27609259, 300.48474687]
    expected_alt = [52.57749508, 51.85943046, 51.13723016]
    az, alt = src._source_get_az_alt(source, times)
    assert np.allclose(az, expected_az)
    assert np.allclose(alt, expected_alt)

def test_source_get_blocks():
    source = 'sun'
    t0 = dt.datetime(2023, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc)
    t1 = dt.datetime(2023, 1, 1, 12, 0, 0, tzinfo=dt.timezone.utc)
    blocks = src.source_get_blocks(source, t0, t1)
    assert blocks == [
        src.SourceBlock(
            t0=dt.datetime(2022, 12, 31, 9, 48, 9, 902594, tzinfo=dt.timezone.utc),
            t1=dt.datetime(2022, 12, 31, 16, 34, 11, 308132, tzinfo=dt.timezone.utc),
            name='sun',
            mode='rising'
        ),
        src.SourceBlock(
            t0=dt.datetime(2022, 12, 31, 16, 34, 11, 308132, tzinfo=dt.timezone.utc),
            t1=dt.datetime(2022, 12, 31, 23, 20, 7, 342350, tzinfo=dt.timezone.utc),
            name='sun',
            mode='setting'
        ),
        src.SourceBlock(
            t0=dt.datetime(2023, 1, 1, 9, 48, 48, 46183, tzinfo=dt.timezone.utc),
            t1=dt.datetime(2023, 1, 1, 16, 34, 39, 671616, tzinfo=dt.timezone.utc),
            name='sun',
            mode='rising'
        ),
        src.SourceBlock(
            t0=dt.datetime(2023, 1, 1, 16, 34, 39, 671616, tzinfo=dt.timezone.utc),
            t1=dt.datetime(2023, 1, 1, 23, 20, 25, 379071, tzinfo=dt.timezone.utc),
            name='sun',
            mode='setting'
        )
    ]

def test_precomputed_source():
    t0 = dt.datetime(2023, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc)
    t1 = dt.datetime(2023, 1, 1, 12, 0, 0, tzinfo=dt.timezone.utc)
    source = src._PrecomputedSource.for_('uranus', t0=t0, t1=t1, buf=dt.timedelta(days=0))
    assert isinstance(source, src._PrecomputedSource)
    assert len(source.blocks) == 4

    t = int(dt.datetime(2023, 1, 1, 5, 0, 0, tzinfo=dt.timezone.utc).timestamp())
    assert np.allclose(source.interp_az(t), [295.34634092])
    assert np.allclose(source.interp_alt(t), [15.48141435])

    assert 'uranus' in src.PRECOMPUTED_SOURCES

def test_source_block():
    srcblk = src.SourceBlock(
        t0=dt.datetime(2023, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc),
        t1=dt.datetime(2023, 1, 1, 12, 0, 0, tzinfo=dt.timezone.utc),
        name='sun',
        mode='rising'
    )
    assert isinstance(srcblk, src.SourceBlock)

    with pytest.raises(ValueError):
        srcblk = src.SourceBlock(
            t0=dt.datetime(2023, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc),
            t1=dt.datetime(2023, 1, 1, 12, 0, 0, tzinfo=dt.timezone.utc),
            name='sun',
            mode='rise'
        )

def test_source_gen_seq():
    blocks = src.source_gen_seq('uranus', dt.datetime(2023, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc), dt.datetime(2023, 1, 1, 12, 0, 0, tzinfo=dt.timezone.utc))
    assert blocks == [
        src.SourceBlock(
            t0=dt.datetime(2023, 1, 1, 0, 0, tzinfo=dt.timezone.utc),
            t1=dt.datetime(2023, 1, 1, 0, 40, 38, 505632, tzinfo=dt.timezone.utc),
            name='uranus',
            mode='rising'
        ),
        src.SourceBlock(
            t0=dt.datetime(2023, 1, 1, 0, 40, 38, 505632, tzinfo=dt.timezone.utc),
            t1=dt.datetime(2023, 1, 1, 6, 14, 17, 34180, tzinfo=dt.timezone.utc),
            name='uranus',
            mode='setting'
        )
    ]

def test_source_block_get_az_alt():
    srcblk = src.SourceBlock(
        t0=dt.datetime(2023, 1, 1, 0, 40, 38, tzinfo=dt.timezone.utc),
        t1=dt.datetime(2023, 1, 1, 1, 14, 17, tzinfo=dt.timezone.utc),
        name='uranus',
        mode='setting'
    )
    times, az, alt = src.source_block_get_az_alt(srcblk)
    assert len(times) == 67
    assert np.allclose(az[:5], [83.97807382, 395.73085271, 349.995829, 362.00775543, 358.54644389])
    assert np.allclose(alt[:5], [51.01782363, 51.01763853, 51.01706878, 51.01611489, 51.01477258])
