import tensorflow as tf

from neupy.core.properties import ProperFractionProperty, NumberProperty
from .base import MinibatchGradientDescent


__all__ = ('Adam',)


class Adam(MinibatchGradientDescent):
    """
    Adam algorithm.

    Parameters
    ----------
    beta1 : float
        Decay rate. Value need to be between ``0`` and ``1``.
        Defaults to ``0.95``.

    beta2 : float
        Decay rate. Value need to be between ``0`` and ``1``.
        Defaults to ``0.95``.

    epsilon : float
        Value need to be greater than ``0``. Defaults to ``1e-5``.

    step : float
        Learning rate, defaults to ``0.001``.

    {MinibatchGradientDescent.batch_size}

    {GradientDescent.addons}

    {ConstructibleNetwork.connection}

    {ConstructibleNetwork.error}

    {BaseNetwork.show_epoch}

    {BaseNetwork.shuffle_data}

    {BaseNetwork.epoch_end_signal}

    {BaseNetwork.train_end_signal}

    {Verbose.verbose}

    Attributes
    ----------
    {MinibatchGradientDescent.Attributes}

    Methods
    -------
    {MinibatchGradientDescent.Methods}

    Examples
    --------
    >>> import numpy as np
    >>> from neupy import algorithms
    >>>
    >>> x_train = np.array([[1, 2], [3, 4]])
    >>> y_train = np.array([[1], [0]])
    >>>
    >>> mnet = algorithms.Adam((2, 3, 1))
    >>> mnet.train(x_train, y_train)
    """
    step = NumberProperty(default=0.001, minval=0)
    beta1 = ProperFractionProperty(default=0.9)
    beta2 = ProperFractionProperty(default=0.999)
    epsilon = NumberProperty(default=1e-7, minval=0)

    def init_train_updates(self):
        updates = []

        epoch = self.variables.epoch
        step = self.variables.step

        for layer, parameter, gradient in self.iter_params_and_grads():
            prev_first_moment = tf.Variable(
                tf.zeros(parameter.shape),
                name="{}/prev-first-moment".format(parameter.op.name),
                dtype=tf.float32,
            )
            prev_second_moment = tf.Variable(
                tf.zeros(parameter.shape),
                name="{}/prev-second-moment".format(parameter.op.name),
                dtype=tf.float32,
            )

            first_moment = (
                self.beta1 * prev_first_moment +
                (1. - self.beta1) * gradient)
            second_moment = (
                self.beta2 * prev_second_moment +
                (1. - self.beta2) * gradient ** 2
            )

            first_moment_bias_corrected = first_moment / (
                1. - self.beta1 ** epoch)

            second_moment_bias_corrected = (
                second_moment / (1. - self.beta2 ** epoch))

            parameter_delta = first_moment_bias_corrected * (
                tf.sqrt(second_moment_bias_corrected + self.epsilon)
            )

            updates.extend([
                (prev_first_moment, first_moment),
                (prev_second_moment, second_moment),
                (parameter, parameter - step * parameter_delta),
            ])

        return updates
