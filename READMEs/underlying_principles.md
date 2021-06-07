# Underlying Principles

## Why/What?
It can be computationaly expensive to produce MC samples, especially if detector simulation is included. This problem becomes even more intractable when performing studies where a set of MC samples are needed at various model benchmark points, e.g. for different values of a Wilson coefficient in an EFT. Thankfully, reweighting schemes exist which can be used to produce the whole set of samples with time nearly equal to the time taken to produce just one benchmark point.

Typically, this sort of reweighting is performed during the MC production. This repo allows one to reweight nanoAOD MC samples **after** their production. This is very useful for analyses which study theories that are SM-like because centrally-produced SM NanoAODSIM can be reweighted with this tool to produce the BSM MC samples. The analysers need not produce MC, only to reweight it, which presents a far quicker way to produce the BSM MC.

## How?
This are 3 fundamental parts to the chain:
1. MadGraph's standalone reweighting module (python interface to matrix elements)
2. EFT2Obs's helper interface (input event info and returns reweights)
3. This NanoAOD-tools module (extracting event info)

Given a compatible model and a process line, MadGraph can output a standalone reweighting module which is essentially a python interface to the squared matrix elements. To make it easier to work with, EFT2Obs provides an additional interface layer which given the relevant event information, will return the reweights. That leaves this nanoAOD-tools module to extract the information from the nanoAOD.

## Neccessary event information
The information needed to reweight an event is:
1. Particle four-momenta
2. Particle PDG id
3. Particle status (incoming or outgoing)
4. Particle helicity*
5. Event $\alpha_s$

*Reweighting can still be performed without helicity information by summing over the possible helicity states, however, this can lead to inaccurate reweighting.

The particles that are required are the same as those defined in the process line that was originally used to make MadGraph's standalone reweighting module. So for a process line like:
```
generate g g > h j
```
you would need to *find* the two incoming gluons and then the resulting Higgs and jet. Anymore particles found in the event are not needed and can be disregarded. 

In nanoAOD there are two potential to *find* the event information: the LHEPart or GenPart branches/collections. LHEPart contains the hard-interaction information which is the same information MadGraph would use to perform the reweighting if it was done during the MC production. For this reason, using the LHEPart collection is usually preferable. However, there are cases where using LHEPart is not possible. For example, if one is interested in BSM effects in the Higgs decay, the reweighting would require information about the decay products  but the decay of the Higgs boson is usually done at the parton-shower stage and hence the decay products are often not included in LHEPart. 

GenPart is an alternative. GenPart will contain all the particles you could probably need, which is great, but it will contain too many particles. Hence, one needs to select the particles that are needed by the reweighting and filter out the rest. In some cases, the user may need to define this filtering process themselves. The code is written to try and make this as easy as possible and an example of doing this is shown in [here](READMEs/making_adjustments.md). An additional disadvantage to using GenPart is that helicity information is not included which can lead to less accurate reweights. Whilst there are downsides to using GenPart, it may be the only possibility for reasons described before.

