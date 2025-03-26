from programs.emecpmaster import EMECPmaster, EMECPmasterParameters

def main():
    params = EMECPmasterParameters(
        nml = EMECPmasterParameters.NML(
            npx = 500,
            dmin = 0.05,
            copyfromenergyfile = 'undefined',
            energyfile = 'GaN/EMECPmaster/_default/EMECPmaster.h5',
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

    prog = EMECPmaster(config=params)
    prog.generate_config()

if __name__ == "__main__":
    main()