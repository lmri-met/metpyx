# Verification of MetPyX numerical values against the values of a reference case
import pytest

from metpyx.data import Coefficients
from metpyx.data import OperationalQuantities
from metpyx.data import Qualities
from metpyx.sim import Spectrum, Quality, QualitySensitivity


class TestDataValues:
    # Data subpackage
    # Reference case for verification:
    # - N60 radiation quality.
    # - H*(10) operational quantity at 0º irradiation angle.
    # - mass energy transfer coefficients for air from PENELOPE 2018.
    # - air kerma to dose conversion coefficients from CMI 2025.

    def test_quality_data(self):
        # Quality class

        # Quality instance
        qualities = Qualities()

        # Quality methods
        is_quality = qualities.is_quality('N60')
        series = qualities.get_series('N60')
        voltage = qualities.get_voltage('N60')
        total_filtration = qualities.get_filtration('N60')
        inherent_filtration = qualities.get_filtration('N60', inherent=True)
        additional_filtration = qualities.get_filtration('N60', additional=True)

        # Assertions
        assert is_quality is True
        assert series == 'N'
        assert voltage == 60
        assert total_filtration == {'Al': 4, 'Cu': 0.6}
        assert inherent_filtration == {'Al': 4}
        assert additional_filtration == {'Cu': 0.6}

    def test_quantity_data(self):
        # OperationalQuantities class

        # OperationalQuantities instance
        quantities = OperationalQuantities()

        # OperationalQuantities methods
        is_quantity = quantities.is_quantity('h_star_10')
        is_quantity_angle = quantities.is_quantity_angle('h_star_10', 0)
        metadata = quantities.get_quantity('h_star_10')
        angles = quantities.get_irradiation_angles('h_star_10')
        symbol = quantities.get_symbol('h_star_10')

        # Assertions
        assert is_quantity is True
        assert is_quantity_angle is True
        assert metadata == {'symbol': 'H*(10)', 'type': 'ambient', 'depth': 10, 'phantom': None, 'angles': [0]}
        assert angles == [0]
        assert symbol == 'H*(10)'

    def test_coefficient_data(self):
        # Coefficients class

        # Coefficients instance
        coefficients = Coefficients()

        # Coefficients methods
        mu = coefficients.get_mu_tr_over_rho_air()
        h_k = coefficients.get_h_k(quantity='h_star_10', angle=0)

        # Reference values for PENELOPE 2018 mass energy transfer coefficients for air
        pene_2018_energies = [
            1.0, 1.1726, 1.25, 1.4, 1.5, 1.75, 2.0, 2.5, 3.0, 3.2063, 3.206301, 3.22391, 3.25051, 3.5, 3.61881, 4.0,
            5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 12.5, 14.0, 15.0, 17.5, 20.0, 25.0, 28.6633, 30.0, 35.0, 40.0, 50.0, 60.0,
            70.0, 80.0, 90.0, 100.0, 125.0, 140.0, 150.0, 175.0, 187.083, 200.0, 250.0, 300.0, 324.037, 350.0, 386.867,
            400.0, 474.342, 500.0, 574.456, 600.0, 673.537, 700.0, 800.0, 900.0, 1000.0, 1250.0, 1500.0, 1558.93,
            1750.0, 1870.83, 2000.0, 2345.21, 2500.0, 3000.0, 3240.37, 3500.0, 4000.0, 4500.0, 5000.0, 6000.0, 6480.74,
            7000.0, 8000.0, 9000.0
        ]
        pene_2018_values = [
            3487.7, 2271.66, 1907.85, 1396.25, 1152.41, 746.85, 510.495, 267.712, 156.677, 128.597, 139.322, 139.22,
            136.749, 110.244, 99.9467, 74.3863, 38.3165, 22.1387, 13.8638, 9.20954762864289, 6.40746485225397,
            4.62692014996195, 2.30743153037744, 1.61505075253763, 1.30130979037554, 0.801145676760343,
            0.525990443101652, 0.262079759969996, 0.17213944380102, 0.150643910752649, 0.096166283094939,
            0.067006659158694, 0.040350724533314, 0.030060380204255, 0.025736225862943, 0.023919178948042,
            0.023273564441493, 0.023169137685326, 0.023905175732908, 0.024501233602389, 0.024926643691358,
            0.025877217107796, 0.026274062287156, 0.026655131026205, 0.027882238669658, 0.028683812435718,
            0.028972447929017, 0.029148771809045, 0.029415131704691, 0.029490249846129, 0.029698178702551,
            0.029685041261757, 0.029603764611649, 0.029549718949812, 0.029405101930449, 0.029197657857256,
            0.028890614121642, 0.028390536220701, 0.027936798166738, 0.026719405747041, 0.02562121786982,
            0.025359438553807, 0.02463108715039, 0.024240842040503, 0.023753744772526, 0.022671649894621,
            0.022309768351513, 0.021132688079239, 0.020639133403572, 0.020121558259145, 0.019347638398287,
            0.018700741656237, 0.018185053120065, 0.017326066208925, 0.016966042150857, 0.016690444038446,
            0.016199645451199, 0.015809252632524
        ]
        # Reference values for CMI 2025 air kerma to dose conversion coefficients for H*(10) at 0º irradiation angle.
        cmi_2025_energies_h_star_10_0 = [
            2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40,
            42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 65, 70, 75, 80, 85, 90, 95, 100, 110, 120, 130, 140, 150, 160, 170,
            180, 190, 200, 225, 240, 250, 275, 300, 325, 350, 375, 400, 425, 450, 500, 511, 550, 600, 662, 700, 800,
            900, 1000, 1117, 1173, 1250, 1332, 1500, 1700, 1750, 2000, 2400, 2500, 3000, 3500, 4000, 4440, 5000, 6000,
            6129, 7000, 8000, 9000, 10000, 12500, 15000, 17500, 20000, 25000, 30000, 35000, 40000, 45000, 50000
        ]
        cmi_2025_values_h_star_10_0 = [
            0.0, 0.0, 0.0, 0.0, 0.0, 5.006211183e-07, 7.53411188163e-05, 0.0013399279666727, 0.008339974116065,
            0.027959365493142, 0.0649015031392173, 0.117892384153277, 0.182854496500547, 0.254785065497812,
            0.329684376352027, 0.404237490435794, 0.474883646496535, 0.543075936619701, 0.608764764690923,
            0.729121699136139, 0.834359989357258, 0.932217912526701, 1.019787991814, 1.10127304871649, 1.17923580150499,
            1.25093929821867, 1.31693499152686, 1.37836679008758, 1.43614832274801, 1.48895147535783, 1.53695987736966,
            1.579367978262, 1.61683555911064, 1.65111364109003, 1.67895036865187, 1.70147532324998, 1.71959205780654,
            1.73569389238546, 1.7513548512875, 1.7660601751939, 1.76411105061724, 1.75880008458157, 1.74401588142437,
            1.7259083944068, 1.7051120882291, 1.68285949300524, 1.660806895852, 1.62069771752482, 1.58655624975128,
            1.55253890207103, 1.5214025670048, 1.49292559713724, 1.47191391445754, 1.45095250563087, 1.43234388256437,
            1.41504458319957, 1.40045048056932, 1.36708755516683, 1.35062396617274, 1.34112411144134, 1.31829850613254,
            1.29920469418009, 1.28280551309179, 1.26779645957562, 1.25550014309865, 1.24492592905825, 1.23453216595746,
            1.225707899164, 1.2113467185313, 1.20789939579853, 1.19806539226821, 1.18818337262196, 1.17653859236809,
            1.17219827416785, 1.16041231542684, 1.14984262965137, 1.14263898967494, 1.13414788332302, 1.13119321285273,
            1.12823105732118, 1.12464830688625, 1.11896627040591, 1.11357509036097, 1.11227237543666, 1.1077193167192,
            1.10088553317439, 1.09989918128124, 1.09354396763082, 1.08802563926124, 1.08425634507853, 1.07995815186229,
            1.07712879613375, 1.0702298390959, 1.06941454173716, 1.06406552317947, 1.05908367593344, 1.05411440308156,
            1.05022231792777, 1.04082044834368, 1.03355131530843, 1.02708988121954, 1.02235595808979, 1.01449765630958,
            1.00889446838262, 1.00286377763245, 1.00129856074053, 0.997193631804752, 0.996021011235643
        ]
        # Assertions
        assert list(mu[0]) == pene_2018_energies
        assert list(mu[1]) == pene_2018_values
        assert list(h_k[0]) == cmi_2025_energies_h_star_10_0
        assert list(h_k[1]) == cmi_2025_values_h_star_10_0


class TestSimulationIntegralQuantitiesValues:
    # Simulation subpackage
    # Reference case for verification:
    # - N60 radiation quality.
    # - Anode angle of 20º.
    # - H*(10) operational quantity at 0º irradiation angle.
    # - mass energy transfer coefficients for air from PENELOPE 2018.
    # - air kerma to dose conversion coefficients from CMI 2025.
    # - measurement distance at 1 m.
    # - air thickness equal to distance.

    @pytest.fixture()
    def ref_values(self):
        # See "verification_sim_integral_quantities.ipynb" for details on how these values were obtained.
        ref = {
            'e_mean': 47.63300484905786,
            'kerma': 1.5821240129760867,
            'hvl1_al': 5.8582747051770605,
            'hvl1_cu': 0.23236896040944352,
            'hvl2_al': 6.196968255804022,
            'hvl2_cu': 0.25978939890001607,
            'hk_mean': 1.5652667635344535,
            'dose': 2.476446133301221,
            'spectrum': {
                'energies': [1.25, 1.75, 2.25, 2.75, 3.25, 3.75, 4.25, 4.75, 5.25, 5.75, 6.25, 6.75, 7.25, 7.75, 8.25,
                             8.75, 9.25, 9.75, 10.25, 10.75, 11.25, 11.75, 12.25, 12.75, 13.25, 13.75, 14.25, 14.75,
                             15.25, 15.75, 16.25, 16.75, 17.25, 17.75, 18.25, 18.75, 19.25, 19.75, 20.25, 20.75, 21.25,
                             21.75, 22.25, 22.75, 23.25, 23.75, 24.25, 24.75, 25.25, 25.75, 26.25, 26.75, 27.25, 27.75,
                             28.25, 28.75, 29.25, 29.75, 30.25, 30.75, 31.25, 31.75, 32.25, 32.75, 33.25, 33.75, 34.25,
                             34.75, 35.25, 35.75, 36.25, 36.75, 37.25, 37.75, 38.25, 38.75, 39.25, 39.75, 40.25, 40.75,
                             41.25, 41.75, 42.25, 42.75, 43.25, 43.75, 44.25, 44.75, 45.25, 45.75, 46.25, 46.75, 47.25,
                             47.75, 48.25, 48.75, 49.25, 49.75, 50.25, 50.75, 51.25, 51.75, 52.25, 52.75, 53.25, 53.75,
                             54.25, 54.75, 55.25, 55.75, 56.25, 56.75, 57.25, 57.75, 58.25, 58.75, 59.25, 59.75],
                'fluence': [0.0, 0.0, 0.0, 0.0, 0.0, 1.4676028957427891e-292, 1.1795457828260624e-205,
                            1.7537208213874036e-149, 1.561405069738898e-111, 5.606990558315252e-85,
                            8.034877187831423e-66, 1.11024989773344e-51, 8.699147853337677e-41, 8.60477955638111e-33,
                            3.1272508438424094e-25, 3.3819844496625376e-21, 1.2604404881262039e-70,
                            9.550257119529037e-60, 1.2907263424469652e-52, 1.0132858639353455e-45,
                            2.1395876812523597e-39, 1.2004511315182753e-34, 1.9040384244645345e-30,
                            9.759230920201159e-27, 1.7100366342989054e-23, 1.1670569205426722e-20,
                            3.509601212870103e-18, 5.273516408095043e-16, 4.421177184807118e-14, 2.246872967630718e-12,
                            7.32051197053362e-11, 1.6252510885484728e-09, 2.5897396954374614e-08, 3.112926284178132e-07,
                            2.9231773575221977e-06, 2.1986933667376068e-05, 0.00013677746578874496,
                            0.000715312030505872, 0.0032130940738165953, 0.012608908092595907, 0.04381522812360861,
                            0.1365998825745206, 0.3867489190733121, 1.004236177809356, 2.4107709601721226,
                            5.392200350164786, 11.314693118012679, 22.408516411052368, 42.13283055519239,
                            75.56076364735678, 129.7398864677207, 214.10434465890063, 340.74386205309236,
                            523.3410714319684, 779.2386644531938, 1128.6302231405814, 1593.6158967166925,
                            2198.1456570641944, 2964.308385296038, 3915.194726251159, 5077.288473861802,
                            6473.459825237774, 8124.366159429419, 10048.250773550111, 12259.642417038116,
                            14769.246788951055, 17583.133402209587, 20702.882732555467, 24091.359867912404,
                            27730.8169691638, 31638.411189150447, 35797.337706716105, 40186.169578232344,
                            44780.591753263194, 49553.410024256846, 54476.415303364694, 59517.56725935673,
                            64642.32099042438, 69741.31263576042, 74769.36136230217, 79761.04794926509,
                            84684.6249697218, 89511.1198612955, 94201.78081946434, 98725.60857286639, 103049.0262056479,
                            107139.7450724601, 110971.33727995686, 114420.72048542189, 117459.29373261011,
                            120159.79856488785, 122498.28885640194, 124451.8824749172, 126005.8418403056,
                            127154.09032367198, 127869.51668021726, 128133.09695557802, 127928.02979073265,
                            127160.79154057032, 125833.04830837694, 124037.50151282363, 121750.14253333083,
                            118960.4499939194, 115655.21347441807, 111825.84890566602, 107465.90720307703,
                            102581.49301555309, 97148.47144437008, 91097.23289782333, 84408.61025777712,
                            77117.3018653684, 69217.73342032309, 60711.82991928426, 51598.111479645755,
                            41869.724741666185, 31528.941520839973, 20641.682513537744, 8116.67056711454]
            }
        }
        return ref

    def test_spectrum_values(self, ref_values):
        # Spectrum instance
        ms = Spectrum(kvp=60, th=20)
        ms.multi_filter([["Al", 4.0], ["Cu", 0.6], ["Air", 1000]])

        # Spectrum
        spectrum = ms.get_spectrum(diff=False)
        assert list(spectrum[0]) == pytest.approx(ref_values['spectrum']['energies'])
        assert list(spectrum[1]) == pytest.approx(ref_values['spectrum']['fluence'])

        # Quality related integral quantities (not related to dose)
        assert ms.get_emean() == pytest.approx(ref_values['e_mean'])
        assert ms.get_kerma() == pytest.approx(ref_values['kerma'])
        assert ms.get_hvl1() == pytest.approx(ref_values['hvl1_al'])
        assert ms.get_hvl2() == pytest.approx(ref_values['hvl2_al'])
        assert ms.get_hvl1(matl="Cu") == pytest.approx(ref_values['hvl1_cu'])
        assert ms.get_hvl2(matl="Cu") == pytest.approx(ref_values['hvl2_cu'])

        # Mean conversion coefficient
        assert ms.get_hk_mean('h_star_10', 0) == pytest.approx(ref_values['hk_mean'])

        # Dose equivalent
        assert ms.get_dose_equivalent('h_star_10', 0) == pytest.approx(ref_values['dose'])

    def test_quality_values(self, ref_values):
        # Quality instance
        mq = Quality("N60", th=20)

        # Quality attributes
        assert mq.quality == 'N60'
        assert mq.voltage == 60
        assert mq.total_filtration == {'Al': 4.0, 'Cu': 0.6}
        assert mq.distance == 100
        assert mq.spek_filtration == [["Al", 4.0], ["Cu", 0.6], ["Air", 1000]]

        # Spectrum
        spectrum = mq.get_spectrum(diff=False)
        assert list(spectrum[0]) == pytest.approx(ref_values['spectrum']['energies'])
        assert list(spectrum[1]) == pytest.approx(ref_values['spectrum']['fluence'])

        # Quality related integral quantities (not related to dose)
        assert mq.get_emean() == pytest.approx(ref_values['e_mean'])
        assert mq.get_kerma() == pytest.approx(ref_values['kerma'])
        assert mq.get_hvl1() == pytest.approx(ref_values['hvl1_al'])
        assert mq.get_hvl2() == pytest.approx(ref_values['hvl2_al'])
        assert mq.get_hvl1(matl="Cu") == pytest.approx(ref_values['hvl1_cu'])
        assert mq.get_hvl2(matl="Cu") == pytest.approx(ref_values['hvl2_cu'])

        # Mean conversion coefficient
        assert mq.get_hk_mean('h_star_10', 0) == pytest.approx(ref_values['hk_mean'])

        # Dose equivalent
        assert mq.get_dose_equivalent('h_star_10', 0) == pytest.approx(ref_values['dose'])


class TestSimulationQuantitiesSensitivityValues:
    # Simulation subpackage
    # Reference case for verification:
    # - N60 radiation quality.
    # - Anode angle of 20º.
    # - H*(10) operational quantity at 0º irradiation angle.
    # - mass energy transfer coefficients for air from PENELOPE 2018.
    # - air kerma to dose conversion coefficients from CMI 2025.
    # - measurement distance at 1 m.
    # - air thickness equal to distance.
    # - Deviation of 5% in tube voltage,
    # - Deviation of 5% in additional filtration thickness
    # - Deviation of 5% of Pb in additional filtration purity.

    def test_perturbed_high_voltage_initialization(self):
        q = QualitySensitivity('N60', 'tube_voltage', 5, th=20)

        # Perturbation attributes
        assert q.quality == 'N60'
        assert q.parameter == 'tube_voltage'
        assert q.deviation == 5
        assert q.material is None
        assert q.distance == 100

        # Nominal parameters
        assert q.nominal_params['tube_voltage'] == 60
        assert q.nominal_params['inherent_filtration'] == {'Al': 4}
        assert q.nominal_params['additional_filtration'] == {'Cu': 0.6}
        assert q.nominal_params['total_filtration'] == {'Al': 4, 'Cu': 0.6}
        assert q.nominal_params['spek_filtration'] == [["Al", 4.0], ["Cu", 0.6], ["Air", 1000]]

        # Perturbed parameters
        assert q.perturbed_params['tube_voltage'] == 60 * 1.05  # +5%
        assert q.perturbed_params['inherent_filtration'] == {'Al': 4}  # No change
        assert q.perturbed_params['additional_filtration'] == {'Cu': 0.6}  # No change
        assert q.perturbed_params['total_filtration'] == {'Al': 4, 'Cu': 0.6}  # No change
        assert q.perturbed_params['spek_filtration'] == [["Al", 4.0], ["Cu", 0.6], ["Air", 1000]]  # No change

        # Nominal spectrum
        assert q.nominal_spec.state.spectrum_parameters.z == 100
        assert q.nominal_spec.state.model_parameters.th == 20
        assert q.nominal_spec.state.model_parameters.kvp == 60
        assert q.nominal_spec.state.filtration.filters == [("Al", 4.0), ("Cu", 0.6), ("Air", 1000)]

        # Perturbed spectrum
        assert q.perturbed_spec.state.spectrum_parameters.z == 100
        assert q.perturbed_spec.state.model_parameters.th == 20
        assert q.perturbed_spec.state.model_parameters.kvp == 60 * 1.05  # +5%
        assert q.perturbed_spec.state.filtration.filters == [("Al", 4.0), ("Cu", 0.6), ("Air", 1000)]

    def test_perturbed_additional_filtration_thickness_initialization(self):
        q = QualitySensitivity("N60", 'additional_filtration_thickness', 5, th=20)

        # Perturbation attributes
        assert q.quality == 'N60'
        assert q.parameter == 'additional_filtration_thickness'
        assert q.deviation == 5
        assert q.material is None
        assert q.distance == 100

        # Nominal parameters
        assert q.nominal_params['tube_voltage'] == 60
        assert q.nominal_params['inherent_filtration'] == {'Al': 4}
        assert q.nominal_params['additional_filtration'] == {'Cu': 0.6}
        assert q.nominal_params['total_filtration'] == {'Al': 4, 'Cu': 0.6}
        assert q.nominal_params['spek_filtration'] == [["Al", 4.0], ["Cu", 0.6], ["Air", 1000]]

        # Perturbed parameters
        assert q.perturbed_params['tube_voltage'] == 60  # No change
        assert q.perturbed_params['inherent_filtration'] == {'Al': 4}  # No change
        assert q.perturbed_params['additional_filtration'] == {'Cu': 0.6 * 1.05}  # +5%
        assert q.perturbed_params['total_filtration'] == {'Al': 4, 'Cu': 0.6 * 1.05}  # +5% in additional
        assert q.perturbed_params['spek_filtration'] == [["Al", 4.0], ["Cu", 0.6 * 1.05], ["Air", 1000]]  # +5% in additional

        # Nominal spectrum
        assert q.nominal_spec.state.spectrum_parameters.z == 100
        assert q.nominal_spec.state.model_parameters.th == 20
        assert q.nominal_spec.state.model_parameters.kvp == 60
        assert q.nominal_spec.state.filtration.filters == [("Al", 4.0), ("Cu", 0.6), ("Air", 1000)]

        # Perturbed spectrum
        assert q.perturbed_spec.state.spectrum_parameters.z == 100
        assert q.perturbed_spec.state.model_parameters.th == 20
        assert q.perturbed_spec.state.model_parameters.kvp == 60
        assert q.perturbed_spec.state.filtration.filters == [("Al", 4.0), ("Cu", 0.6 * 1.05), ("Air", 1000)] # +5%

    def test_perturbed_additional_filtration_purity_initialization(self):
        q = QualitySensitivity("N60", 'additional_filtration_purity', 5, material='Pb', th=20)

        # Perturbation attributes
        assert q.quality == 'N60'
        assert q.parameter == 'additional_filtration_purity'
        assert q.deviation == 5
        assert q.material == 'Pb'
        assert q.distance == 100

        pb_thick = 0.6*(0.05*8.96)/(0.95*11.35)

        # Nominal parameters
        assert q.nominal_params['tube_voltage'] == 60
        assert q.nominal_params['inherent_filtration'] == {'Al': 4}
        assert q.nominal_params['additional_filtration'] == {'Cu': 0.6}
        assert q.nominal_params['total_filtration'] == {'Al': 4, 'Cu': 0.6}
        assert q.nominal_params['spek_filtration'] == [["Al", 4.0], ["Cu", 0.6], ["Air", 1000]]

        # Perturbed parameters
        assert q.perturbed_params['tube_voltage'] == 60  # No change
        assert q.perturbed_params['inherent_filtration'] == {'Al': 4}  # No change
        assert q.perturbed_params['additional_filtration'] == {'Cu': 0.6, 'Pb': pb_thick}  # +5%
        assert q.perturbed_params['total_filtration'] == {'Al': 4, 'Cu': 0.6, 'Pb': pb_thick}  # +5% in additional
        assert q.perturbed_params['spek_filtration'] == [["Al", 4.0], ["Cu", 0.6], ["Pb", pb_thick], ["Air", 1000]]  # +5% in additional

        # Nominal spectrum
        assert q.nominal_spec.state.spectrum_parameters.z == 100
        assert q.nominal_spec.state.model_parameters.th == 20
        assert q.nominal_spec.state.model_parameters.kvp == 60
        assert q.nominal_spec.state.filtration.filters == [("Al", 4.0), ("Cu", 0.6), ("Air", 1000)]

        # Perturbed spectrum
        assert q.perturbed_spec.state.spectrum_parameters.z == 100
        assert q.perturbed_spec.state.model_parameters.th == 20
        assert q.perturbed_spec.state.model_parameters.kvp == 60
        assert q.perturbed_spec.state.filtration.filters == [("Al", 4.0), ("Cu", 0.6), ("Pb", pb_thick), ("Air", 1000)] # +5%
