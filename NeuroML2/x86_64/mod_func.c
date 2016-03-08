#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _Golgi_KV_reg(void);
extern void _Golgi_Na_reg(void);
extern void _Golgi_NaT_reg(void);
extern void _Input_Golgi_pop0_0_reg(void);
extern void _Input_Golgi_pop0_1_reg(void);
extern void _Input_Golgi_pop1_0_reg(void);
extern void _Input_Golgi_pop1_1_reg(void);
extern void _LeakCond_reg(void);
extern void _MFSpikeSyn_reg(void);
extern void _gap_junction00_reg(void);
extern void _iaf1_reg(void);
extern void _iaf2_reg(void);
extern void _pulseGen0_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," Golgi_KV.mod");
    fprintf(stderr," Golgi_Na.mod");
    fprintf(stderr," Golgi_NaT.mod");
    fprintf(stderr," Input_Golgi_pop0_0.mod");
    fprintf(stderr," Input_Golgi_pop0_1.mod");
    fprintf(stderr," Input_Golgi_pop1_0.mod");
    fprintf(stderr," Input_Golgi_pop1_1.mod");
    fprintf(stderr," LeakCond.mod");
    fprintf(stderr," MFSpikeSyn.mod");
    fprintf(stderr," gap_junction00.mod");
    fprintf(stderr," iaf1.mod");
    fprintf(stderr," iaf2.mod");
    fprintf(stderr," pulseGen0.mod");
    fprintf(stderr, "\n");
  }
  _Golgi_KV_reg();
  _Golgi_Na_reg();
  _Golgi_NaT_reg();
  _Input_Golgi_pop0_0_reg();
  _Input_Golgi_pop0_1_reg();
  _Input_Golgi_pop1_0_reg();
  _Input_Golgi_pop1_1_reg();
  _LeakCond_reg();
  _MFSpikeSyn_reg();
  _gap_junction00_reg();
  _iaf1_reg();
  _iaf2_reg();
  _pulseGen0_reg();
}
