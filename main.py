from programs.emmcopencl import EMMCOpenCLParameters, EMMCOpenCL
from programs.emecpmaster import EMECPmasterParameters, EMECPmaster
from programs.emecp import EMECPParameters, EMECP
from programs.emecci import EMECCIParameters, EMECCI

def main():
    EMMCOpenCLParams = EMMCOpenCLParameters(
        nml=EMMCOpenCLParameters.NML(
            mode = 'bse1',
            xtalname = 'GaN.xtal',
            numsx = 501,
            sig = 70.0,
            omega = 0.0,
            sigstart = 0.0,
            sigend = 30.0,
            sigstep = 2.0,
            ivolx = 1001,
            ivoly = 1001,
            ivolz = 101,
            ivolstepx = 1.0,
            ivolstepy = 1.0,
            ivolstepz = 1.0,
            num_el = 10,
            platid = 1,
            devid = 1,
            globalworkgrpsz = 150,
            totnum_el = 200,
            multiplier = 1,
            EkeV = 15.0,
            Ehistmin = 14.0,
            Ebinsize = 1.0,
            depthmax = 100.0,
            depthstep = 1.0,
            dataname = 'EMMCOpenCL/EMMCOpenCL.h5',
            Notify = 'Off'
        )
    )

    EMECPmasterParams = EMECPmasterParameters(
        nml = EMECPmasterParameters.NML(
            npx = 500,
            dmin = 0.5,
            copyfromenergyfile = 'undefined',
            energyfile = 'EMECPmaster/EMECPmaster.h5',
            combinesites = False,
            Notify = 'Off',
            nthreads = 12
        ),
        bethe = EMECPmasterParameters.BETHE(
            c1 = 4.0,
            c2 = 8.0,
            c3 = 50.0,
            sgdbdiff = 1.00
        )
    )

    EMECPParams = EMECPParameters(
        nml = EMECPParameters.NML(
             xtalname = 'GaN.xtal',
            npix = 256,
            thetac = 5.0,
            maskpattern = 'n',
            energyfile = 'EMECP/EMECPmaster.h5',
            masterfile = 'EMECP/EMECPmaster.h5',
            anglefile = 'EMECP/Euler.txt',
            eulerconvention = 'hkl',
            gammavalue = 1.0,
            outputformat = 'bin',
            datafile = 'EMECP/EMECP.h5',
            tiff_prefix = 'undefined',
            nthreads = 12,
            sampletilt = 0.0,
            workingdistance = 13.0,
            Rin = 2.0,
            Rout = 6.0,
            fn_f = '0,0,1',
            fn_s = '0,0,1',
            xtalname2 = 'undefined',
            gF = '0,0,0',
            gS = '0,0,0',
            tF = '0,0,0',
            tS = '0,0,0',
            dmin = 0.025,
            filmthickness = 0.0,
            filmfile = 'undefined',
            subsfile = 'undefined'
        ),
        euler = EMECPParameters.EULER(
            type = 'eu',
            num = 1,
            angles = '0,0,0'
        )
    )

    EMECCIParameters(
        nml = EMECCIParameters.NML(
            nthreads = 12,
            voltage = 15.,
            xtalname = 'GaN.xtal',
            progmode = 'array',
            summode = 'diag',
            k = '0,0,1',
            dkt = 1.5,
            ktmax = 3.0,
            lauec = '0.0, 0.0',
            lauec2 = '0.0, 0.0',
            nktstep = 20,
            dmin = 0.5,
            defectfilename = 'EMECCI/EMdefect.json',
            dataname = 'EMECCI/EMECCI.h5',
            ECPname = 'EMECCI/EMECP.h5',
            montagename = 'EMECCI/EMECCI.tiff',
            DF_L = 1.0,
            DF_npix = 256,
            DF_npiy = 256,
            DF_slice = 1.0
        ),
        bethe = EMECPmasterParameters.BETHE(
            c1 = 4.0,
            c2 = 8.0,
            c3 = 50.0,
            sgdbdiff = 1.00
        )
    )

    EMMCOpenCLProgram = EMMCOpenCL(config=EMMCOpenCLParams)
    EMMCOpenCLProgram.generate_config()
    EMMCOpenCLProgram.run()

    EMECPmasterProgram = EMECPmaster(config=EMECPmasterParams)
    EMECPmasterProgram.copy_output_file(EMMCOpenCLProgram, "EMECPmaster")
    EMECPmasterProgram.generate_config()
    EMECPmasterProgram.run()

    EMECPProgram = EMECP(config=EMECPParams)
    EMECPProgram.copy_output_file(EMECPmasterProgram)
    EMECPProgram.generate_config()
    EMECPProgram.run()

    EMECCIProgram = EMECCI(config=EMECCIParameters)
    EMECCIProgram.copy_output_file(EMECPProgram)
    EMECCIProgram.generate_config()
    EMECCIProgram.run()


if __name__ == "__main__":
    main()