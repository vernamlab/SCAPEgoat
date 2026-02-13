"""
File: TemplateAttack.py
Author: Lil Peeler (lbpeeler@wpi.edu)
Date: 02-12-2026
Description: Functions to implement a template attack using HW classes. Includes GE visualization.
"""

import numpy as np
import matplotlib.pyplot as plt

SBOX = np.array([
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16
], dtype=np.uint8)

HW = np.array([bin(n).count("1") for n in range(256)], dtype=np.uint8)

def compute_hw_labels(pts, key_byte, byte=0):
    ptb = pts[:, byte]
    sbox_out = SBOX[np.bitwise_xor(ptb, key_byte)]
    return np.array([HW[v] for v in sbox_out])


def build_hw_templates(traces, pts, key_byte, byte, cov_mode="pooled"):
    """
    Builds templates using given mode
    cov_mode:
      "diag": Diagonal covariance (only an estimator)
      "full": Standard
      "pooled": Shared covariance across all HW classes
    """
    
    labels = compute_hw_labels(pts, key_byte, byte)
    templates = {}
    
    REG_VALUE = 1e-4    #regularization
    D = traces.shape[1]   #cov matrix dimension
    
    if cov_mode == "pooled":    #shared; does not need to be recomputed per class
        pooled_cov = np.cov(traces, rowvar=False) + REG_VALUE * np.eye(D)
        
        inv_cov = np.linalg.inv(pooled_cov)
        _, logdet = np.linalg.slogdet(pooled_cov)

    for l in range(9):  #HW 0 - 8
        mask = (labels == l)
        if mask.sum() < 10:
            continue
        
        # print(f"HW {l}: {mask.sum()} samples")                #for DEBUG, check size of class
        X = traces[mask]
        mu = X.mean(axis=0)
        
        if cov_mode == "diag":
            var = X.var(axis=0) + 1e-6
            templates[l] = (mu, var)
        elif cov_mode == "full":
            #precompute for mem
            cov = np.cov(X, rowvar=False) + REG_VALUE * np.eye(D)
            # cond = np.linalg.cond(cov)                        #for DEBUG, check condition num of cov matrix
            # print(f"matrix condition number: {cond:.2e}")
            
            inv_cov = np.linalg.inv(cov)
            _, logdet = np.linalg.slogdet(cov)
            
            templates[l] = (mu, inv_cov, logdet)
        else:
            templates[l] = (mu, inv_cov, logdet)

    return templates

def logpdf_diag(X, mu, var):
    if X.ndim == 1:
        X = X.reshape(1, -1)

    return -0.5*np.sum(np.log(var)+((X - mu)**2)/var, axis=1)

def logpdf_full(X, mu, inv_cov, logdet):
    D = mu.shape[0]
    diff = X - mu
    quad = np.sum(diff @ inv_cov*diff, axis=1)
    return -0.5*(D*np.log(2*np.pi)+logdet+quad)

def ge_curve_single_run(
    templates,
    atk_traces,
    atk_pts,
    correct_key,
    byte,
    step=20,
    cov_mode="pooled"
):
    n_attack = atk_traces.shape[0]
    scores = np.zeros(256)
    ge_curve = []

    for n in range(step, n_attack+1, step):
        start = n - step        #new only
        end   = n

        atk_newchunk = atk_traces[start:end]
        pt_newchunk = atk_pts[start:end]

        for k in range(256):
            labels = compute_hw_labels(pt_newchunk, k, byte)

            ll = 0
            for l, params in templates.items():
                mask = (labels == l)
                if mask.sum() == 0:
                    continue

                if cov_mode == "diag":
                    mu, var = params
                    ll += logpdf_diag(atk_newchunk[mask], mu, var).sum()
                
                else:
                    mu, inv_cov, logdet = params
                    ll += logpdf_full(atk_newchunk[mask], mu, inv_cov, logdet).sum()

            scores[k] += ll

        ranked = np.argsort(scores)[::-1]
        rank = np.where(ranked == correct_key)[0][0]
        ge_curve.append(rank)

    return np.array(ge_curve)


def template_attack(
    prof_traces,
    prof_plaintexts,
    atk_traces,
    atk_plaintexts,
    correct_key_byte,
    byte_index=0,
    cov_mode="pooled",
    n_trials=10,
    n_atk_subset=None,
    step=10,
    visualize=True
):
    """
    Runs full template attack
    :prof_traces : Profiling traces
    :prof_plaintexts : Plaintexts for profiling traces
    :atk_traces : Attack traces
    :atk_plaintexts : Plaintexts for attack traces
    :correct_key_byte : 
    :byte_index : byte to attack
    :cov_mode : Mode for covariance calculation, "diag", "full", or "pooled"
    :n_trials : number of trials
    :n_atk_subset : number of attack traces to use in each trial
    :step : Step size for GE evaluation
    :visualize : Whether to plot GE
    :return: dict with GE curve for each trial, avg GE across trials, final rank of correct key in each trial, sorted list of key guesses

    """    
    mean = prof_traces.mean(axis=0)
    std = prof_traces.std(axis=0) + 1e-9
    prof_traces = (prof_traces - mean) / std
    atk_traces = (atk_traces - mean) / std
    
    # build templates
    templates = build_hw_templates(
        prof_traces,
        prof_plaintexts,
        correct_key_byte,
        byte_index,
        cov_mode=cov_mode
    )
    
    print("Templates built")
    
    # set default subset size to all
    if n_atk_subset is None:
        n_atk_subset = atk_traces.shape[0]
    
    all_ge_curves = []
    final_ranks = []
    n_attack = atk_traces.shape[0]
    
    if visualize:
        plt.figure(figsize=(9,6))
    
    for t in range(n_trials):
        print(f"Trial {t+1}/{n_trials}")
        
        idx = np.random.choice(n_attack, n_atk_subset, replace=False)
        perm = np.random.permutation(n_atk_subset)
        
        tr_sub = atk_traces[idx][perm]
        pt_sub = atk_plaintexts[idx][perm]
        
        ge = ge_curve_single_run(
            templates,
            tr_sub,
            pt_sub,
            correct_key_byte,
            byte_index,
            step=step,
            cov_mode=cov_mode
        )
        
        all_ge_curves.append(ge)
        final_ranks.append(ge[-1])
        
        if visualize:
            # plot current trial
            x_axis = np.arange(step, step*len(ge)+1, step)
            plt.plot(x_axis, ge, alpha=0.35)
    
    if visualize:
        plt.axhline(0, linestyle='--')
        plt.xlabel("Attack Traces")
        plt.ylabel("Guessing Entropy (Rank)")
        plt.title("Individual Trials")
        plt.grid(True)
        plt.show()
        
        all_ge_curves = np.array(all_ge_curves)
        avg_ge = all_ge_curves.mean(axis=0)
        
        plt.figure(figsize=(9,6))
        x_axis = np.arange(step, step*len(avg_ge)+1, step)
        plt.plot(x_axis, avg_ge, marker='o', linewidth=2)
        plt.axhline(0, linestyle='--')
        plt.xlabel("Attack Traces")
        plt.ylabel("Average Guessing Entropy")
        plt.title("Average GE Across Trials")
        plt.grid(True)
        plt.show()
    
    #compute final key ranking (using all attack traces)
    scores = np.zeros(256)
    for k in range(256):
        labels = compute_hw_labels(atk_plaintexts, k, byte_index)  # Use ALL
        ll = 0
        for l, params in templates.items():
            mask = (labels == l)
            if mask.sum() == 0:
                continue
            if cov_mode == "diag":
                mu, var = params
                ll += logpdf_diag(atk_traces[mask], mu, var).sum()  # Use ALL
            else:
                mu, inv_cov, logdet = params
                ll += logpdf_full(atk_traces[mask], mu, inv_cov, logdet).sum()  # Use ALL
        scores[k] = ll
    
    key_ranking = np.argsort(scores)[::-1]
    
    return {
        'ge_curves': np.array(all_ge_curves),
        'avg_ge': np.array(all_ge_curves).mean(axis=0),
        'final_ranks': np.array(final_ranks),
        'key_ranking': key_ranking
    }