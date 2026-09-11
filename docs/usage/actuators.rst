Identified actuators
====================

The Vstone VS-S055 and VS-S055C do not appear in this table yet. Separate
fit-ready actuator boundaries are available as ``vstone_vs_s055`` and
``vstone_vs_s055c``, but no physically identified friction parameter JSON is
bundled for either model. Communication support remains scoped to VS-S055;
VS-S055C protocol compatibility is unverified.

Published VS-S055 product specification
---------------------------------------

Vstone publishes the following product data for the normal-cable VS-S055.
The immutable reference record is available as
``bam.vstone.VS_S055_SPECIFICATION``.

.. list-table::
    :header-rows: 1
    :widths: 32 68

    * - Item
      - Published value
    * - Listed price
      - JPY 4,000 before tax
    * - Dimensions
      - 19.6 (W) × 35.8 (D) × 25.0 (H) mm
    * - Mass
      - Approximately 19.6 g
    * - Servo output torque
      - 5.5 kgf·cm at 7.2 V
    * - Operating speed
      - 0.16 s/60° at 7.4 V
    * - Motion range
      - 300°
    * - Supply voltage
      - 4.8–7.4 V
    * - Control methods listed by Vstone
      - TTL command and PWM
    * - Serial interface
      - Up to 230.4 kbps, TTL half-duplex, Futaba serial command compatible
    * - Sensor information
      - Angle, torque, temperature
    * - Calibration
      - 31 points
    * - Package contents
      - Servo, horn, horn screw, ADH servo connector (200 mm)

Source: `Vstone VS-S055 product specifications
<https://www.vstone.co.jp/products/vs_s055/index.html>`_. These values are
reference metadata, not identified BAM values for motor constants, resistance,
controller gain, inertia, or friction. ``VstoneBus`` currently implements only
the TTL serial command path; the table's PWM entry does not represent a PWM
transport implemented by this package. Equivalent numerical values are not
assigned to VS-S055C because a standalone manufacturer specification has not
been confirmed.

Each motor below ships with pre-identified friction parameters. Click a motor
to browse its JSON parameters, or use the **Use in MuJoCo** / **Use in mjlab**
buttons to jump to the integration guide with the code examples pre-filled for
that motor.

.. list-table::
    :header-rows: 1
    :widths: 14 14 18 28 26
    :class: actuators-table

    * - Actuator
      - Image
      - Name
      - Description
      - Use in simulation

    * - **MX-64**
      - .. image:: ../_static/actuator_mx64.png
            :width: 120px

      - ``mx64``
      - ROBOTIS Dynamixel MX-64 servo-actuator
        (`Parameters <https://github.com/Rhoban/bam/tree/main/bam/params/mx64>`__,
        `model <https://github.com/Rhoban/bam/blob/main/bam/dynamixel/actuator.py>`__,
        `raw data <https://huggingface.co/buckets/Gregwar/bam_data/resolve/mx64_raw.tgz?download=true>`__)
      - .. raw:: html

           <a class="sd-btn sd-btn-outline-primary motor-btn" href="mujoco_cpu.html?motor=mx64">Use in MuJoCo</a>
           <a class="sd-btn sd-btn-outline-primary motor-btn" href="mjlab_gpu.html?motor=mx64">Use in mjlab</a>

    * - **MX-106**
      - .. image:: ../_static/actuator_mx106.png
            :width: 120px

      - ``mx106``
      - ROBOTIS Dynamixel MX-106 servo-actuator
        (`Parameters <https://github.com/Rhoban/bam/tree/main/bam/params/mx106>`__,
        `model <https://github.com/Rhoban/bam/blob/main/bam/dynamixel/actuator.py>`__,
        `raw data <https://huggingface.co/buckets/Gregwar/bam_data/resolve/mx106_raw.tgz?download=true>`__)
      - .. raw:: html

           <a class="sd-btn sd-btn-outline-primary motor-btn" href="mujoco_cpu.html?motor=mx106">Use in MuJoCo</a>
           <a class="sd-btn sd-btn-outline-primary motor-btn" href="mjlab_gpu.html?motor=mx106">Use in mjlab</a>

    * - **XL-320**
      - .. image:: ../_static/actuator_xl320.png
            :width: 120px

      - ``xl320``
      - ROBOTIS Dynamixel XL-320 servo-actuator
        (`Parameters <https://github.com/Rhoban/bam/tree/main/bam/params/xl320>`__,
        `model <https://github.com/Rhoban/bam/blob/main/bam/dynamixel/actuator.py>`__)
      - .. raw:: html

           <a class="sd-btn sd-btn-outline-primary motor-btn" href="mujoco_cpu.html?motor=xl320">Use in MuJoCo</a>
           <a class="sd-btn sd-btn-outline-primary motor-btn" href="mjlab_gpu.html?motor=xl320">Use in mjlab</a>

    * - **XL-330**
      - .. image:: ../_static/actuator_xl330.png
            :width: 120px

      - ``xl330``
      - ROBOTIS Dynamixel XL-330 servo-actuator
        (`Parameters <https://github.com/Rhoban/bam/tree/main/bam/params/xl330>`__,
        `model <https://github.com/Rhoban/bam/blob/main/bam/dynamixel/actuator.py>`__,
        `raw data <https://huggingface.co/buckets/Gregwar/bam_data/resolve/xl330_raw.zip?download=true>`__)
      - .. raw:: html

           <a class="sd-btn sd-btn-outline-primary motor-btn" href="mujoco_cpu.html?motor=xl330">Use in MuJoCo</a>
           <a class="sd-btn sd-btn-outline-primary motor-btn" href="mjlab_gpu.html?motor=xl330">Use in mjlab</a>

    * - **STS3215 (7.4V)**
      - .. image:: ../_static/actuator_feetech_sts3215_7_4V.png
            :width: 120px

      - ``feetech_sts3215_7_4V``
      - Feetech STS3215 servo-actuator (7.4V version)
        (`Parameters <https://github.com/Rhoban/bam/tree/main/bam/params/feetech_sts3215_7_4V>`__,
        `model <https://github.com/Rhoban/bam/blob/main/bam/feetech/actuator.py>`__,
        `raw data <https://huggingface.co/buckets/Gregwar/bam_data/resolve/feetech_sts3215_raw.zip?download=true>`__)
      - .. raw:: html

           <a class="sd-btn sd-btn-outline-primary motor-btn" href="mujoco_cpu.html?motor=feetech_sts3215_7_4V">Use in MuJoCo</a>
           <a class="sd-btn sd-btn-outline-primary motor-btn" href="mjlab_gpu.html?motor=feetech_sts3215_7_4V">Use in mjlab</a>

    * - **ST3025**
      - .. image:: ../_static/actuator_waveshare_st3025.png
            :width: 120px

      - ``waveshare_st3025``
      - Waveshare ST3025 12 V serial bus servo-actuator
        (`Parameters <https://github.com/Rhoban/bam/tree/main/bam/params/waveshare_st3025>`__,
        `model <https://github.com/Rhoban/bam/blob/main/bam/waveshare/actuator.py>`__,
        `raw data <https://github.com/i1Cps/duck_mini_pro_headless/releases/download/st3025-bam-data-v1/waveshare_st3025_raw.zip>`__)
      - .. raw:: html

           <a class="sd-btn sd-btn-outline-primary motor-btn" href="mujoco_cpu.html?motor=waveshare_st3025">Use in MuJoCo</a>
           <a class="sd-btn sd-btn-outline-primary motor-btn" href="mjlab_gpu.html?motor=waveshare_st3025">Use in mjlab</a>
