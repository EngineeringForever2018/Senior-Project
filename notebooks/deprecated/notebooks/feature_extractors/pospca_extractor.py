import numpy as np
from numpy import ndarray

from notebooks.feature_extractors.base_feature_extractor import BaseFeatureExtractor
from notebooks.utils import split_text
from notebooks.feature_extractors import pospca_helpers as avpd


class POSPCAExtractor(BaseFeatureExtractor):
    def __init__(self, paragraph_length, n_components):
        self.paragraph_length = paragraph_length
        self.n_components = n_components

    def extract(self, text: str) -> ndarray:
        paragraphs = split_text(text, sentences_per_split=self.paragraph_length)

        # Add Phi samples (x-xBar) to Phi, stored as a list for ease of use but imagine its a 2D array stored vertically
        X_list = []
        for paragraph in paragraphs:
            X_list.append(avpd.make_X(paragraph))

        # From that calculate the average
        xBar = avpd.make_xBar(X_list)

        # Store Phi into a list, just imagine they're vertically stored in a 2D array and not a list of 1D arrays
        Phi_list = avpd.make_PhiList(X_list, xBar)

        # From Phi, calculate A used for...
        A = avpd.make_A(Phi_list)

        # Calculating the covariance matrix
        SigmaX = avpd.make_covarianceMatrix(A)

        # And from the covariance Matrix, SigmaX, we can calculate the eigenvector and eigenvector coefficients
        lamb, v = avpd.make_Eigen(SigmaX)
        # in this application, v is synonymous with my report's u_i = A v_i, because we dont have to do the multiplication and
        # what not

        # For ease, we're storing v into a list of 1D arrays similar to how Phi is stored and then normalizing them
        vList = avpd.store_v(v)
        avpd.normalize_vList(vList)

        # And from that we can make our omega list, or y_i as its referred to in the report
        omegaList = avpd.make_omegaList(Phi_list, vList)

        # return omegaList

        x_matrix = np.concatenate([np.expand_dims(x, 0) for x in X_list])

        return np.matmul(x_matrix, v[:, : self.n_components])

        # Determine T threshold and get k eigenvectors
        T = 0.99
        k = avpd.get_kThresh(lamb, T)

        # PhiHat = avpd.get_PhiHat(k, omegaList, vList)

        sample_String = "We can then find the Euclidean distance between Phi_hat and Phi to determine how good of a fit the model is.  The lower the Euclidean distance, the more similar the projected and original picture are.  The Euclidean distance is found using Equation 9 below."

        while True:
            # print(xBar)
            PhiHat = avpd.get_PhiHat(avpd.get_kThresh(lamb, T), omegaList, vList)
            print("Current score: ", avpd.test_String(sample_String, xBar, PhiHat))
            cmd = input("\nIntegrate (y/n)? ")
            if cmd == "n":
                print("Quitting...")
                break
            elif cmd == "y":
                print("Integrating...")
                (
                    X_List,
                    xBar,
                    Phi_list,
                    A,
                    lamb,
                    vList,
                    omegaList,
                ) = avpd.integrate_String(
                    sample_String, X_list, xBar, Phi_list, A, lamb, vList, omegaList
                )
            else:
                print("Command not found. Use y/n")

        # But to check, have class 1 and class 2 stuff: all essays vs THIS essay

        # for i in SigmaX:
        #    print(i)
        # print(avpd.case3_BDT(avpd.make_X(sample_String), X_list, SigmaX, 0.5))
